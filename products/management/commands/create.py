from itertools import cycle

from django.core.management.base import BaseCommand
from faker import Faker
from faker_commerce import Provider, CATEGORIES, PRODUCT_DATA
from model_bakery import baker

from products.models import Category, Product, Tag, Size

class Command(BaseCommand):
    help = 'Create random categories'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')
        
    def handle(self, *args, **kwargs):
        # get quantity
        total = kwargs['total']

        # faker to create data
        fake = Faker()

        # add commerce to faker
        fake.add_provider(Provider)

        # add categories
        # get categories
        tags = Tag.objects.all()
        categories = Category.objects.all()
        size = Size.objects.all()

        if categories.count() < 22:
            # add categories
            baker.make('products.Category', name=cycle(CATEGORIES), _quantity=22)
            categories = Category.objects.all()

        if tags.count() < 22:
            # add subcategories
            baker.make('products.Tag', name=cycle(CATEGORIES),  _quantity=22)
            tags = Tag.objects.all()
            
        if size.count() < 22:
            # add subcategories
            baker.make('products.Size', name=fake.random.choice(["S", "M", "X"]), stock=fake.random_int(1, 600),  _quantity=22)
            size = Size.objects.all()

        # add products
        for _ in range(total):
            baker.make('products.Product',
                    sku=fake.ean13(),
                    name=f"{fake.random.choice(PRODUCT_DATA['adjective'])} {fake.random.choice(PRODUCT_DATA['product'])}", 
                    price=fake.random_int(30, 200),
                    stripe_price=fake.ean13(),
                    discount=fake.random_int(0, 40),
                    is_new=fake.boolean(),
                    rating=fake.random_int(2, 5),
                    sale_count=fake.random_int(1, 600), 
                    category=cycle(categories), 
                    tag=cycle(tags), 
                    short_description=fake.paragraph(nb_sentences=50),
                    full_description=fake.paragraph(nb_sentences=100),
                    
                    )
        products = Product.objects.all()
        for p in products:
            baker.make('products.Image', products = p, image=fake.file_path(category='image'))
            baker.make('products.Variation', products = p, color=fake.color_name(), image=fake.file_path(category='image'), size=cycle(size))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} products'))