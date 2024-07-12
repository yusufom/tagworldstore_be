from django.contrib import admin
from .models import Product, Category, Size, Variation, Tag, Image, WishList, ProductReview
from django.utils.safestring import mark_safe



class VariationAdmin(admin.TabularInline):
    model = Variation
    extra = 1
    
class ImagesAdmin(admin.TabularInline):
    model = Image
    extra = 1

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
  list_display = ("product_image", "name", "price", "stock", "is_active")
  inlines = [VariationAdmin, ImagesAdmin]
  prepopulated_fields = {"slug": ("name",)}
  
  def product_image(self, obj):
    first_image = obj.image.first()
    if first_image:
      return mark_safe("<img src='{url}' width='50' height='50' />".format(
              url = first_image.image.url
              )
      )
    return "-"
  
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
admin.site.register(ProductReview)
admin.site.register(Tag, TagAdmin)