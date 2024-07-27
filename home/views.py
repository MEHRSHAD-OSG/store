from django.shortcuts import render , get_object_or_404 ,redirect
from django.views import View
from . import models
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin
from orders import forms
# Create your views here.


class HomeView(View):
    def get(self,request,category_slug=None):
        products = models.Product.objects.filter(available=True)
        categories = models.Category.objects.filter(is_sub=False)
        if category_slug:
            # use get because filter return query set
            category= models.Category.objects.get(slug=category_slug)
            # same name with top product
            products = products.filter(category=category)
        return render(request,'home/home.html',{'products':products,'category':categories})


class ProductDetailView(View):
    def get(self,request,slug):
        product = get_object_or_404(models.Product,slug=slug)
        form = forms.CartForms()
        return render(request,'home/detail.html',{'product':product,'form':form})


class BucketHomeView(IsAdminUserMixin,View):
    template_name = 'home/bucket.html'

    def get(self,request):
        objects = tasks.all_bucket_objects_task()
        return render(request,self.template_name,{'objects': objects})


class DeleteBucketObjectView(IsAdminUserMixin,View):
    def get(self,request,key):
        tasks.delete_object_task.delay(key)
        messages.success(request,"your object will be delete soon...","info")
        return redirect('home:bucket')


class DownloadBucketObjectView(IsAdminUserMixin,View):
    def get(self,request,key):
        tasks.download_object_task.delay(key)
        messages.success(request,"your download will start soon...","info")
        return redirect('home:bucket')