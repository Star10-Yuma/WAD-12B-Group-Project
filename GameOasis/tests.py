from django.test import TestCase, Client
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from .views import *
import json
# Create your tests here.
class HomeViewTest(TestCase):
    # Checks that a logged in user can add items to cart and when the user logs out the cart is empty
    def test_home_view_authenticated_user(self):
        user = User.objects.create_user(username='testuser', password='12345')
        customer = Customer.objects.create(user = user, name='Jake', email='Jake@gmail.com')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('GameOasis:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GameOasis/home.html')
        self.assertEqual(response.context['cartItems'], 0)


        order = OrderCart.objects.get(customer=customer)
        category = Category.objects.create(name='testCategory')
        product = Product.objects.create(name='Test Product', price = 99.99, category=category)
        OrderItem.objects.create(product=product, order_cart=order, quantity=1)

        response = self.client.get(reverse('GameOasis:home'))
        self.assertEqual(response.context['cartItems'], 1)

        self.client.logout()
        response = self.client.get(reverse('GameOasis:home'))
        self.assertEqual(response.context['cartItems'], 0)


    def test_home_view_unauthenticated_user(self):
        response = self.client.get(reverse('GameOasis:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GameOasis/home.html')
        self.assertEqual(response.context['cartItems'], 0)


class ContactUsViewTest(TestCase):
    #This checks that the contactus page exists in the website
    def test_contactus_view(self):
        response = self.client.get(reverse('GameOasis:contactus'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GameOasis/contactus.html')

class ShopViewTest(TestCase):
    # This checks that the user can see the shop page, see the products within it and redirects him to login page if he logs out
    def test_shop_view_authenticated_user(self):
        user = User.objects.create_user(username='testuser', password='12345')
        customer = Customer.objects.create(user=user, name='Jake', email='Jake@gmail.com')
        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('GameOasis:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GameOasis/shop.html')
        self.assertEqual(len(response.context['products']), 0)

        category = Category.objects.create(name='testCategory')
        productOne = Product.objects.create(name='Test Product 1', price = 99.99, category=category)
        productTwo = Product.objects.create(name='Test Product 2', price = 50.00, category=category)
        response = self.client.get(reverse('GameOasis:shop'))
        self.assertEqual(len(response.context['products']), 2)

    def test_shop_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('GameOasis:shop'))
        self.assertRedirects(response, '/GameOasis/login/?next=/GameOasis/shop/')


class CartViewTest(TestCase):
    #Checks that user can see cart, can see the total number of items and takes him to the login page if he's not logged in
    def test_cart_view_authenticated_user(self):
        user = User.objects.create_user(username='testuser', password='12345')
        customer = Customer.objects.create(user=user, name='Jake', email='Jake@gmail.com')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('GameOasis:cart'))
        self.assertTemplateUsed(response, 'GameOasis/cart.html')
        self.assertEqual(response.context['cartItems'], 0)



        order = OrderCart.objects.get(customer=customer)
        category = Category.objects.create(name='testCategory')
        productOne = Product.objects.create(name='Test Product 1', price=99.99, category=category)
        productTwo = Product.objects.create(name='Test Product 2', price=50.00, category=category)
        OrderItem.objects.create(product=productOne, order_cart=order, quantity=3)
        OrderItem.objects.create(product=productTwo, order_cart=order, quantity=2)

        response = self.client.get(reverse('GameOasis:cart'))
        self.assertEqual(response.context['cartItems'], 5)
        self.assertEqual(response.context['order'], order)

    def test_cart_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('GameOasis:cart'))
        self.assertRedirects(response, reverse('GameOasis:login'))


class CheckoutView(TestCase):
    #Checks if the checkout page is showing all added products and shows nothing if user is logged out
    def test_checkout_view_authenticated_user(self):
        user = User.objects.create_user(username='testuser', password='12345')
        customer = Customer.objects.create(user=user, name='Jake', email='Jake@gmail.com')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('GameOasis:checkout'))


        category = Category.objects.create(name='testCategory')
        productOne = Product.objects.create(name='Test Product 1', price=99.99, category=category)
        productTwo = Product.objects.create(name='Test Product 2', price=50.00, category=category)
        order = OrderCart.objects.get(customer=customer)
        OrderItem.objects.create(product=productOne, order_cart=order, quantity=2)
        OrderItem.objects.create(product=productTwo, order_cart=order, quantity=2)


        response = self.client.get(reverse('GameOasis:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GameOasis/checkout.html')
        self.assertEqual(response.context['cartItems'], 4)
        self.assertFalse(response.context['shipping'], False)

    def test_checkout_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('GameOasis:checkout'))
        self.assertEqual(response.context['cartItems'], 0)

class UpdateItemView(TestCase):
    #Checks if you can add and remove product quantity in the cart page
    def test_setup_user_cart(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Jake', email='Jake@gmail.com')
        self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name='testCategory')
        self.product = Product.objects.create(name='Test Product 1', price=99.99, category=self.category, id=1)
        self.order = OrderCart.objects.create(customer=self.customer, is_complete=False)
        self.order_item = OrderItem.objects.create(product=self.product, order_cart=self.order, quantity=2)
    def test_update_item_quantity_add(self):
        self.test_setup_user_cart()
        url = reverse('GameOasis:update_item')
        data = {'productId': self.product.id, 'action': 'add'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, 3)


    def test_update_item_quantity_remove_and_delet(self):
        self.test_setup_user_cart()
        url = reverse('GameOasis:update_item')
        data = {'productId': self.product.id, 'action': 'remove'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, 1)

        data = {'productId': self.product.id, 'action': 'remove'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        with self.assertRaises(OrderItem.DoesNotExist):
            self.order_item.refresh_from_db()

class OrderCompleteView(TestCase):
    #Checks that the order was completed
    def test_setup_user_cart(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Jake', email='Jake@gmail.com')
        self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name='testCategory')
        self.product = Product.objects.create(name='Test Product 1', price=99.99, category=self.category, id=1)
        self.order = OrderCart.objects.create(customer=self.customer, is_complete=False)
        self.order_item = OrderItem.objects.create(product=self.product, order_cart=self.order, quantity=2)

    def test_order_complete(self):
        self.test_setup_user_cart()
        url = reverse('GameOasis:checkout')
        data = {
            'form': {
                'total': '199.98',
            },
            'shipping': {
                'address': '123 Test St',
                'city': 'Testville',
                'country': 'Test',
            },
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

class UserLoginView(TestCase):
    #Checks if user logged in properly or not
    def test_user_login_valid(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Jake', email='Jake@gmail.com')
        url = reverse('GameOasis:login')
        data = {
            'username': 'testuser',
            'password': '12345'
        }
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, 'GameOasis/login_new.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_invalid(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Jake', email='Jake@gmail.com')
        url = reverse('GameOasis:login')
        data = {
            'username': 'testuser',
            'password': '123'
        }
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, 'GameOasis/login_new.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid login details supplied.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class RegisterView(TestCase):
    def test_setup(self):
        self.client = Client()
        self.url = reverse('GameOasis:register')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': '12345'
        }

    def test_register_view_check(self):
        self.test_setup()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GameOasis/register_new.html')

    def test_post_success(self):
        self.test_setup()
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Successful registration!")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_post_failed(self):
        self.test_setup()
        invalid_data = {
            'username': 'testuser',
            'email': 'invalidEmail',
            'password': '12345'
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Successful registration!")

class ViewProductView(TestCase):

    def test_view_product(self):
        self.client = Client()
        self.category = Category.objects.create(name='testCategory')
        self.product = Product.objects.create(name='Test Product 1', price=99.99, category=self.category, id=1)
        url = reverse('GameOasis:view_product', args=[self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GameOasis/view_product.html')
        self.assertEqual(response.context['product'], self.product)

class ShowCategoryView(TestCase):
    def test_show_category(self):
        self.client = Client()
        self.category = Category.objects.create(name='testCategory', id=1)
        self.productOne = Product.objects.create(name='Test Product 1', price=99.99, category=self.category)
        self.productTwo = Product.objects.create(name='Test Product 2', price=49.99, category=self.category)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Jake', email='Jake@gmail.com')
        self.order = OrderCart.objects.create(customer=self.customer, is_complete=False)
        OrderItem.objects.create(product=  self.productTwo , order_cart=self.order , quantity=2)
        OrderItem.objects.create(product=self.productTwo, order_cart=self.order , quantity=2)
        url = reverse('GameOasis:show_category', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'GameOasis/category.html')
        self.assertEqual(response.context['category'], self.category)

    def test_show_category_invalid(self):
        self.client = Client()

        url = reverse('GameOasis:show_category', args=[2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)






















