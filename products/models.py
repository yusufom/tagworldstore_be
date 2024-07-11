from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


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
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price = models.CharField(help_text="price id from stripe", max_length=50)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    offer_end = models.DateTimeField()
    is_new = models.BooleanField(default=False)
    rating = models.IntegerField()
    sale_count = models.IntegerField(blank=True, null=True, default=1)
    stock = models.IntegerField()
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)
    short_description = models.TextField()
    full_description = models.TextField()
    slug = models.SlugField(default="", null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


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