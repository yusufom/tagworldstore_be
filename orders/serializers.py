from rest_framework import serializers
from orders.models import CartItem, Order
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
        
class LineItemSerializer(serializers.Serializer):
    price = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()

class CheckoutSessionSerializer(serializers.Serializer):
    pkid = serializers.UUIDField()
    line_items = LineItemSerializer(many=True)
    
    
class OrderSerializer(serializers.Serializer):
    items = serializers.ListField()
    
    
class ConfirmOrderSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    status = serializers.CharField()
    
    
class ListOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1
        
        
class CreateMulitpleCartItemsSerializer(serializers.Serializer):
    items = serializers.ListField()