from django.contrib import messages

from .models import *
from .forms import *
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):

    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderCart.objects.get_or_create(customer=customer, is_complete=False)
        cartItems = order.calculate_cart_items
    else:
        items = []
        order = {'calculate_cart_total': 0, 'calculate_cart_items': 0, 'shipping': False}
        cartItems = order['calculate_cart_items']

    context['cartItems'] = cartItems

    return render(request, 'GameOasis/home.html', context)

def contactus(request):

    return render(request, 'GameOasis/contactus.html')

@login_required
def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderCart.objects.get_or_create(customer=customer, is_complete=False)
        items = order.orderitem_set.all()
        cartItems = order.calculate_cart_items

        products = Product.objects.all()


    else:
        # if the user is not logged in it sets the cart to 0 to avoid any errors
        items = []
        order = {'calculate_cart_total': 0, 'calculate_cart_items': 0, 'shipping': False}
        cartItems = order['calculate_cart_items']
        return redirect(reverse('GameOasis:login'))

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'GameOasis/shop.html', context)






def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderCart.objects.get_or_create(customer = customer, is_complete=False)
        items = order.orderitem_set.all()
        cartItems = order.calculate_cart_items
        context = {'items': items, 'order': order, 'cartItems': cartItems}

        return render(request, 'GameOasis/cart.html', context)

    #This is for the guest user
    else:
        #if the user is not logged in it sets the cart to 0 to avoid any errors
        items =[]
        order = {'calculate_cart_total': 0, 'calculate_cart_items': 0,'shipping': False}
        cartItems = order['calculate_cart_items']
        return redirect(reverse('GameOasis:login'))






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

def user_login(request):
    if request.method == 'POST':
        #Takes the username and password inputted to authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Using django engine it checks if this combination is valid and returns the User object if it is
        user = authenticate(username=username, password=password)

        #Now if the user object is in our database it will check if it is active or not
        if user:
            if user.is_active:
                #user may login if active
                login(request,user)
                messages.success(request, 'Login success!')
                return render(request, 'GameOasis/login_new.html')

            else:
                #else account inactive so no logging in
                # return HttpResponse("Your account is disabled")
                messages.error(request, 'Your account is disabled.')
                return render(request, 'GameOasis/login_new.html')

        else:
            #invalid login details provided so no logging in
            # return HttpResponse("Invalid login details supplied.")
            messages.error(request, 'Invalid login details supplied.')
            return render(request, 'GameOasis/login_new.html')

    #if the scenario was a HTTP GET
    else:
        #No context variables to return hence blank dictionary object so no third parameter
        return render(request, 'GameOasis/login_new.html')


def register(request):
    #Boolean value to indicate if the registration was successful or not
    #Set to false initially then changes to true when it is successful
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            #Saves the users form data to the database if valid
            user = user_form.save()
            #Now we hash the user password and then update the user object
            user.set_password(user.password)
            user.save()
            customer = Customer.objects.create(user=user, name=user.username, email=user.email)

            #Updated registered to show that the form has been successful
            registered = True
            redirect(reverse('GameOasis:home'))
            messages.success(request, "Successful registration!")
            return render(request, 'GameOasis/register_new.html')

        else:
            #prints any mistakes/invalid forms in the terminal
            print(user_form.errors)
            # messages.error(request, user_form.errors)
            return render(request, 'GameOasis/register_new.html',
                          context={'user_res': user_form.errors, 'registered': registered})

    else:
        #Not a HTTP Post so we render the form using the two ModelForm instances so they are ready for user input
        user_form = UserForm()

    return render(request, 'GameOasis/register_new.html', context = {'user_form': user_form, 'registered': registered})


@login_required
def user_logout(request):
    #Since we know the user is logged in we can now just log them out
    logout(request)
    #Takes the user back to the homepage
    return redirect(reverse('GameOasis:home'))

def view_product(request, product_name_slug):
    try:
        product = Product.objects.get(slug=product_name_slug)

    except Product.DoesNotExist:
        product = None

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderCart.objects.get_or_create(customer=customer, is_complete=False)
        cartItems = order.calculate_cart_items
    else:
        items = []
        order = {'calculate_cart_total': 0, 'calculate_cart_items': 0, 'shipping': False}
        cartItems = order['calculate_cart_items']

    context_dict = {'product': product, 'cartItems': cartItems}
    return render(request, 'GameOasis/view_product.html', context_dict)

def show_category(request, category_id):
        context_dict = {}

        try:
            category = get_object_or_404(Category, id=category_id)
            products = Product.objects.filter(category=category)
            context_dict['category'] = category
            context_dict['products'] = products


        except Category.DoesNotExist:
            context_dict['category'] = None
            context_dict['products'] = None

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = OrderCart.objects.get_or_create(customer=customer, is_complete=False)
            cartItems = order.calculate_cart_items
        else:
            items = []
            order = {'calculate_cart_total': 0, 'calculate_cart_items': 0, 'shipping': False}
            cartItems = order['calculate_cart_items']

        context_dict['cartItems'] = cartItems



        return render(request, 'GameOasis/category.html', context_dict)


