from django.shortcuts import render

# Create your views here.
def home(request):





    return render(request, 'GameOasis/home.html')

def contactus(request):





    return render(request, 'GameOasis/contactus.html')

def shop(request):

    context = {}



    return render(request, 'GameOasis/shop.html', context)



def user_login(request):



    return render(request, 'GameOasis/login.html')



def register(request):



    return render(request, 'GameOasis/register.html')


def category(request):

    return render(request, 'GameOasis/category.html' )


def cart(request):

    return render(request, 'GameOasis/cart.html' )


def checkout(request):

    context = {}



    return render(request, 'GameOasis/checkout.html',context)
