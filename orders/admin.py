from django.contrib import admin

from orders.models import CartItem, Order

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Order)