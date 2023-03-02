from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.
def home(request):





    return render(request, 'GameOasis/home.html')

def contactus(request):





    return render(request, 'GameOasis/contactus.html')

def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderCart.objects.get_or_create(customer=customer, is_complete=False)
        items = order.orderitem_set.all()
        cartItems = order.calculate_cart_items
    else:
        # if the user is not logged in it sets the cart to 0 to avoid any errors
        items = []
        order = {'calculate_cart_total': 0, 'calculate_cart_items': 0, 'shipping': False}
        cartItems = order['calculate_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'GameOasis/shop.html', context)



def user_login(request):



    return render(request, 'GameOasis/login.html')



def register(request):



    return render(request, 'GameOasis/register.html')


def category(request):

    return render(request, 'GameOasis/category.html' )


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderCart.objects.get_or_create(customer = customer, is_complete=False)
        items = order.orderitem_set.all()
        cartItems = order.calculate_cart_items

    #This is for the guest user
    else:
        #if the user is not logged in it sets the cart to 0 to avoid any errors
        items =[]
        order = {'calculate_cart_total': 0, 'calculate_cart_items': 0,'shipping': False}
        cartItems = order['calculate_cart_items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'GameOasis/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderCart.objects.get_or_create(customer=customer, is_complete=False)
        items = order.orderitem_set.all()
        cartItems = order.calculate_cart_items

    else:
        # if the user is not logged in it sets the cart to 0 to avoid any errors
        items = []
        order = {'calculate_cart_total': 0, 'calculate_cart_items': 0}
        cartItems = order['calculate_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}

    return render(request, 'GameOasis/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('ProductId:', productId)
    print('Action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = OrderCart.objects.get_or_create(customer=customer, is_complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order_cart=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def orderComplete(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('Data: ', request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderCart.objects.get_or_create(customer=customer, is_complete=False)
        total = float (data['form']['total'])
        order.transaction_id = transaction_id
        print('Order total', order.calculate_cart_total)

        if total == float(order.calculate_cart_total):
            order.is_complete = True
        print('Order', order.is_complete)
        order.save()

        if order.shipping == True:
            ShippingDetails.objects.create(customer=customer, order_cart=order, address=data['shipping']['address'], city=data['shipping']['city'], country=data['shipping']['country'],)

    else:
        print('User is not logged in..')

    return JsonResponse('Payment complete!', safe=False)



