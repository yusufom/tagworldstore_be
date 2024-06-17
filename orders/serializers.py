from rest_framework import serializers
from orders.models import CartItem
from products.models import Product
from products.serializers import ProductCartSerializer, ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = ProductCartSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product',  'quantity', 'selected_product_color', 'selected_product_size']
        depth = 1
        
class CartItemListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product',  'quantity', 'selected_product_color', 'selected_product_size']
        depth = 1