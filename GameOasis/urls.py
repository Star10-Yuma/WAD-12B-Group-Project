from django.urls import path
from GameOasis import views
from django.urls import include


app_name = 'GameOasis'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('contact-us/', views.contactus, name='contactus'),
    path('shop/', views.shop, name='shop'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('category/', views.category, name='category'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.updateItem, name='update_item'),
    path('order-success/', views.orderComplete, name='orderComplete'),
    path('logout/', views.user_logout, name='logout'),

]