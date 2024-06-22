from django.contrib import admin
from .models import Product, Category, Size, Variation, Tag, Image, WishList, ProductReview



class VariationAdmin(admin.TabularInline):
    model = Variation
    extra = 1
    
class ImagesAdmin(admin.TabularInline):
    model = Image
    extra = 1

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
  list_display = ("name", "price", "sale_count",)
  inlines = [VariationAdmin, ImagesAdmin]
  prepopulated_fields = {"slug": ("name",)}
  
class CategoryAdmin(admin.ModelAdmin):
  list_display = ("name", )
  prepopulated_fields = {"slug": ("name",)}
  
class TagAdmin(admin.ModelAdmin):
  list_display = ("name", )
  prepopulated_fields = {"slug": ("name",)}
  
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size)
admin.site.register(Variation)
admin.site.register(WishList)
admin.site.register(ProductReview)
admin.site.register(Tag, TagAdmin)