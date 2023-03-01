from django.contrib import admin
from .models import Product
from .models import Customer
from .models import Order
from .models import OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'image']

# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
