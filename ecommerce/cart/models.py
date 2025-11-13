from django.db import models
from shop.models import Product
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def subtotal(self):
        return self.product.price*self.quantity


from django.utils import timezone
class Order(models.Model):
    amount=models.IntegerField(null=True)
    order_id=models.CharField(max_length=30,null=True)
    order_date=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.IntegerField()
    address=models.TextField()
    is_ordered=models.BooleanField(default=False)
    payment_method=models.CharField(max_length=30)
    delivery_status=models.CharField(default="pending")
    def __str__(self):
        return self.user.username


class Order_items(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="products")
    quantity=models.IntegerField()
    def __str__(self):
        return self.product.name
