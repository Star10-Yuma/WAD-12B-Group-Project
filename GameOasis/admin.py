from django.contrib import admin
from .models import *
# Register your models here.

#This customises the admin interface
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Update the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderCart)
admin.site.register(OrderItem)
admin.site.register(ShippingDetails)
