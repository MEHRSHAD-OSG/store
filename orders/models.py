from django.db import models
from accounts.models import User
from home.models import Product
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='u_orders')
    paid = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['paid', '-updated']

    def get_total_price(self):
        return sum(item.get_cost() for item in self.order_item.all())

    def __str__(self):
        return str(self.user)



class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_item')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return str(self.product)