from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render ,redirect
from . import models
from django.views import View
from . import forms
import random
from utils import send_otp_code
from django.contrib import messages
from django.utils import timezone
import datetime
# Create your views here.


class UserRegisterView(View):
    form_class = forms.UserRegistrationForm

    def get(self,request):
        form = self.form_class
        return render(request,'accounts/register.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000,9999)
            send_otp_code(form.cleaned_data['phone'],random_code)
            models.OtpCode.objects.create(phone_number=form.cleaned_data['phone'],code=random_code)
            request.session['user_registration_info'] = {
                'phone_number' : form.cleaned_data['phone'],
                'email' : form.cleaned_data['email'],
                'full_name' : form.cleaned_data['full_name'],
                'password' : form.cleaned_data['password']
            }
            messages.success(request,'we sent a code','success')
            return redirect('accounts:verify_code')
        return render(request,'accounts/register.html',{'form':form})


class UserRegisterVerifyCodeView(View):
    form_class = forms.VerifyCodeForm

    def get(self,request):
        form = self.form_class
        return render(request,'accounts/verify.html',{'form':form})

    def post(self,request):
        user_session = request.session['user_registration_info']
        form = self.form_class(request.POST)
        code_instance = models.OtpCode.objects.get(phone_number=user_session['phone_number'])
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                models.User.objects.create_user(
                    phone_number=user_session['phone_number'],
                    email=user_session['email'],
                    full_name=user_session['full_name'],
                    password=user_session['password']
                )
                code_instance.delete()
                messages.success(request,'you registered','success')
                return redirect('home:home')
            messages.error(request,'code is wrong','danger')
            return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLoginView(View):
    form_class = forms.UserLoginForm
    template_name = 'accounts/login.html'

    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        self.next = request.GET.get('next')
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phone_number = cd['phone'],password = cd['password'])
            if user:
                login(request,user)
                messages.success(request,'logged in successfully','success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,'phone number or password is wrong','danger')
        return render(request,self.template_name,{'form':form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')
