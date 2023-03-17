from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique = True)

    #overrides the save method to get to slugify the names of the categories so that the URL can not have spaces in its category names
    def save(self, *args, **kwargs):
        print(self.name, slugify(self.name))
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
#Fixes name from categorys to categories in admin page
    class Meta:
        verbose_name_plural = "Categories"

#Outputs the String name of the category object
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    is_digital = models.BooleanField(default = False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    #overrides the save method to get to slugify the names of the products so that the URL can not have spaces in its category names
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url

        except:
            url = ''

        return url


class OrderCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default = False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.id}"

    @property
    def calculate_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.calculate_total for item in order_items])
        return total

    @property
    def calculate_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for item in order_items:
            if item.product.is_digital == False:
                shipping = True
        return shipping

    def get_order_items(self):
        order_items = self.orderitem_set.all()
        return order_items
    def get_products(self):
        order_items = self.get_order_items()
        products  = [item.product for item in order_items]
        return products


class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    order_cart = models.ForeignKey(OrderCart,on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    item_date_added = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_total(self):
        total = self.quantity * self.product.price
        return total

class ShippingDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_cart = models.ForeignKey(OrderCart,on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


