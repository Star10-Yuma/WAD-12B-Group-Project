import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'websitemain.settings')
from django.core.files import File
from django.template.defaultfilters import slugify

import django

django.setup()
from GameOasis.models import Category, Product


def populate():
    consoles_products = [
        {
            'name': 'PS5',
            'price': 450.99,
            'is_digital': False,
            'image': File(open(os.path.join('static', 'images', 'ps5.jpg'), 'rb')),
            'slug': 'ps5',
        }
    ]

    videogames_products = [
        {
            'name': 'vbucks',
            'price': 99.99,
            'is_digital': True,
            'image': File(open(os.path.join('static', 'images' , 'vbucks.png'), 'rb')),
            'slug': 'vbucks',

        },
        {
            'name': 'fortnite skin',
            'price': 99.99,
            'is_digital': True,
            'image': File(open(os.path.join('static', 'images' , 'R_2.png'), 'rb')),
            'slug': 'fortnite-skin',

        },
        {
            'name': 'God of War',
            'price': 59.99,
            'is_digital': False,
            'image': File(open(os.path.join('static', 'images' , 'god-of-war-ragnarok-ps5_1.jpg'), 'rb')),
            'slug': 'god-of-war',
        }]

    gamingAccessories_products = [
        {
            'name': 'Gaming Headphones',
            'price': 99.99,
            'is_digital': False,
            'image': File(open(os.path.join('static', 'images' , 'logitech.jpg'), 'rb')),
            'slug': 'gaming-headphones',

        },
        {
            'name': 'gaming keyboard',
            'price': 49.99,
            'is_digital': False,
            'image': File(open(os.path.join('static', 'images' , 'Best-cheap-gaming-keyboard-runner-up-Vava-Gaming-Keyboard.png'), 'rb')),
            'slug': 'gaming-keyboard',
        },
        {
            'name': 'gaming mouse',
            'price': 30.99,
            'is_digital': False,
            'image': File(open(os.path.join('static', 'images' , 'mouse.jpg'), 'rb')),
            'slug': 'gaming-mouse',
        }]

    categories = {
        'consoles': {'products': consoles_products},
        'videogames': {'products': videogames_products},
        'accessories': {'products': gamingAccessories_products}
    }

    for categories, categories_data in categories.items():
        print("Adding category", categories)
        c = add_categories(categories)
        print("Added category", categories)
        for p in categories_data['products']:
            add_product(p['name'], p['price'], p['is_digital'], p['image'], c)



    for c in Category.objects.all():
        for p in Product.objects.filter(category=c):
            print(f'- {c}: {p}')
def add_product(name, price, is_digital, image, cat):
    p, created = Product.objects.get_or_create(
        name=name,
        category=cat,
        defaults={
            "price": price,
            "is_digital": is_digital,
            "image": image,
        }
    )
    if not created:
        p.price = price
        p.is_digital = is_digital
        p.image = image
        p.save()

    return p


def add_categories(name):
    print(Category.objects.all())
    c, created = Category.objects.get_or_create(name=name)
    print("saved category", c, created)
    c.save()
    return c

if __name__ == '__main__':
        print('Starting GameOasis population script...')
        populate()
        print("Population Complete")
