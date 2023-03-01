from django.db import models
from django.contrib.auth.models import User
import datetime

class Product(models.Model):
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/products/')


    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device
        return str(name)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateField(default=datetime.datetime.today)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(default=datetime.datetime.today)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

