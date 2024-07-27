from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='scategory',blank=True,null=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category',args=[self.slug])

class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    image = models.ImageField()
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('home:detail', args=[self.slug])

    def __str__(self):
        return self.name