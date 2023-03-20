import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'websitemain.settings')

import django

django.setup()
from GameOasis.models import Category, Product


def populate():
    consoles_products = [
        {
            'name': 'PS5',
            'price': 500.00,
            'is_digital': False,
            'image': 'ps5.jpg',
            'slug': 'ps5',
        },
        {
            'name': 'Xbox Series X',
            'price': 500.00,
            'is_digital': False,
            'image': 'xbox.jpg',
            'slug': 'xbox-series-x',

        }
    ]

    videogames_products = [
        {
            'name': 'vbucks',
            'price': 99.99,
            'is_digital': True,
            'image': 'vbucks.png',
            'slug': 'vbucks',

        },
        {
            'name': 'fortnite skin',
            'price': 99.99,
            'is_digital': True,
            'image': 'R_2.png',
            'slug': 'fortnite-skin',

        },
        {
            'name': 'God of War',
            'price': 59.99,
            'is_digital': False,
            'image': 'god-of-war-ragnarok-ps5_1.jpg',
            'slug': 'god-of-war',
        }]

    gamingAccessories_products = [
        {
            'name': 'Gaming Headphones',
            'price': 99.99,
            'is_digital': False,
            'image': 'logitech.jpg',
            'slug': 'gaming-headphones',

        },
        {
            'name': 'gaming keyboard',
            'price': 49.99,
            'is_digital': False,
            'image': 'Best-cheap-gaming-keyboard-runner-up-Vava-Gaming-Keyboard.png',
            'slug': 'gaming-keyboard',
        },
        {
            'name': 'gaming mouse',
            'price': 30.99,
            'is_digital': False,
            'image': 'mouse.jpg',
            'slug': 'gaming-mouse',
        }]

    categories = {
        'consoles': {'products': consoles_products},
        'videogames': {'products': videogames_products},
        'accessories': {'products': gamingAccessories_products}
    }

    for categories, categories_data in categories.items():
        c = add_categories(categories)
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
    c, created = Category.objects.get_or_create(name=name)
    c.save()
    return c

if __name__ == '__main__':
        print('Starting GameOasis population script...')
        populate()
        print("Population Complete")
