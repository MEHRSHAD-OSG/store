from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']
    ordering = ['name']
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','available']
    raw_id_fields = ['category']
    search_fields = ['name','price']
    ordering = ['name']
    prepopulated_fields = {'slug': ['name']}



