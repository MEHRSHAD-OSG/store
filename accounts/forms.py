from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import string

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords must be match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(max_length=255)
    full_name = forms.CharField(label='full name',max_length=100)
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone(self):
        cd = self.cleaned_data
        for phone in cd['phone']:
            if phone not in string.digits:
                raise ValidationError('Phone number must be integer')
        if len(cd['phone']) != 11:
            raise ValidationError('Phone must be 11')
        user = User.objects.filter(phone_number=cd['phone']).exists()
        if user:
            raise ValidationError('This phone number is already exists')
        OtpCode.objects.filter(phone_number=phone).delete()
        return cd['phone']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone(self):
        cd = self.cleaned_data
        for phone in cd['phone']:
            if phone not in string.digits:
                raise ValidationError('Phone number must be integer')
        if len(cd['phone']) != 11:
            raise ValidationError('Phone must be 11')
        return cd['phone']