from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderCart)
admin.site.register(OrderItem)
admin.site.register(ShippingDetails)