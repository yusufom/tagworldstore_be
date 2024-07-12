from django.contrib import admin

from orders.models import CartItem, Order


class OrderAdmin(admin.ModelAdmin):
  list_display = ("user", "status", "items_count", "item_display",  "shipping_address", "ordered_date", "ordered", "is_paid",)
  list_filter = ["status", "is_paid"]
  list_editable = ('status', )
  search_fields = ["user__email", "ref_code"]
  
  def item_display(self, obj):
      return ", ".join([i.product.name for i in obj.items.all()])
  
  
  item_display.short_description = "Items"
  def items_count(self, obj):
      return obj.items.all().count()
  def has_add_permission(self, request, obj=None):
    return False



# Register your models here.
# admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)