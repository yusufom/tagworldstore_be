from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
import os
from dotenv import load_dotenv



load_dotenv()


import stripe

stripe.api_key = os.environ.get('STRIPE_API_KEY')


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default="", null=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default="", null=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        

        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    

class Size(models.Model):
    name = models.CharField(max_length=10)
    stock = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} ({self.stock})"

class Variation(models.Model):
    color = models.CharField(max_length=50)
    products = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="variation")
    image = models.ImageField(upload_to='assets/img/product/fashion/')
    size = models.ManyToManyField(Size)
    
class Image(models.Model):
    products = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to='assets/img/product/fashion/')

class Product(models.Model):
    sku = models.CharField(max_length=50, blank=True, null=True, help_text="Leave blank, Do not edit")
    name = models.CharField(max_length=255, help_text="Name of item")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of item (in pounds)")
    stripe_price = models.CharField(help_text="Strip pride id, leave blank Do not edit", max_length=50, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage e.g 35 == 35%", default=0)
    offer_end = models.DateTimeField(blank=True, null=True)
    is_new = models.BooleanField(default=False, help_text="If item just arrived in store (New Arrival)")
    rating = models.IntegerField(default=4, help_text="Item rating, out of 5")
    sale_count = models.IntegerField(blank=True, null=True, default=1, help_text="Amount of this item sold")
    stock = models.IntegerField(help_text="Amount of this item currently in stock", default=1)
    category = models.ManyToManyField(Category, help_text="Category of item (This will help with filtering)")
    tag = models.ManyToManyField(Tag, help_text="Tag of item (This will help with filtering)")
    short_description = models.TextField(help_text="Short Description, 250 letters or less")
    full_description = models.TextField(help_text="Full Descriptionn of Item, 250 letters or less")
    slug = models.SlugField(default="", null=False, help_text="Do not edit")
    is_active = models.BooleanField(default=True, help_text="True if Item is to be displayed to customers, False if item should be hidden")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        first_image = self.image.all()
        if not self.stripe_price:
            # Create Stripe product
            stripe_product = stripe.Product.create(
                name=self.name,
                description=self.full_description[:240],
                active=self.is_active,
                images=[image.url for image in first_image] if first_image else []
            )
            # Create Stripe price
            stripe_price = stripe.Price.create(
                currency="gbp",
                unit_amount=int(self.price * 100), 
                product=stripe_product.id
            )
            self.stripe_price = stripe_price.id
            self.sku = stripe_product.id
        else:
            # Update Stripe product
            stripe_product = stripe.Product.modify(
                stripe.Product.retrieve(stripe.Price.retrieve(self.stripe_price).product).id,
                name=self.name,
                description=self.full_description[:240],
                active=self.is_active
            )
            
        super().save(*args, **kwargs)
        
    
    def delete(self, *args, **kwargs):
        # Delete Stripe product
        if self.stripe_price:
            stripe_product_id = stripe.Price.retrieve(self.stripe_price).product
            stripe.Product.delete(stripe_product_id)
        
        super().delete(*args, **kwargs)


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name="wishlist_products")
    
    
    def __str__(self):
        return self.user.email
    
    
class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"