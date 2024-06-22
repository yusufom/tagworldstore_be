from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from products.models import Product, Size, Variation
from .models import CartItem
from .serializers import CartItemSerializer, CartItemListSerializer, CheckoutSessionSerializer
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

import stripe

stripe.api_key = 'sk_test_51PToko2MhBsxnjfBB2l9FXzrFyJJKDRI4BtwE2MJwACUDysEHSInJ0F52vf5DHtOCVrtt84bwZz3BoJazeHiV4oS00VpJL9sch'

YOUR_DOMAIN = 'http://localhost:3000/checkout'



class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user, ordered=False)
        serializer = CartItemListSerializer(cart_items, many=True)
        return Response(serializer.data)

    def create(self, request):
        product_data = request.data.get('product')
        product = Product.objects.get(id=product_data["id"])
        serializer = CartItemSerializer(data=request.data)
        image = product_data["image"]
        user = request.user
        
        if serializer.is_valid():
            try:
                variation = product.variation.get(color=request.data.get('selected_product_color'))
            except Variation.DoesNotExist:
                return Response({"error": "Invalid color selected"}, status=status.HTTP_400_BAD_REQUEST)

            # Find the size stock from the variation
            try:
                size = variation.size.get(name=request.data.get('selected_product_size'))
            except Size.DoesNotExist:
                return Response({"error": "Invalid size selected"}, status=status.HTTP_400_BAD_REQUEST)
            res = serializer.validated_data
            res["product"].update(image=image)
            cart_item = CartItem.objects.filter(
                user=user,
                product=product,
                selected_product_color=request.data.get('selected_product_color'),
                selected_product_size=request.data.get('selected_product_size')
            ).first()
            

            if cart_item:
                cart_item.quantity += request.data.get('quantity', 1)
                if cart_item.quantity > size.stock:
                    return Response({"error": "Not enough stock available"}, status=status.HTTP_400_BAD_REQUEST)
                cart_item.save()
            else:
                serializer.save(product=product, user=user)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(id=pk)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
    def decrease_quantity(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(id=pk)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return Response(status=status.HTTP_200_OK)
            else:
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        user = request.user
        CartItem.objects.filter(user=user, ordered=False).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def create_checkout_session(self, request):
        print(request.data)
        serializer = CheckoutSessionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                checkout_session = stripe.checkout.Session.create(
                    line_items=serializer.validated_data['line_items'],
                    mode='payment',
                    success_url=YOUR_DOMAIN + '?success=true',
                    cancel_url=YOUR_DOMAIN + '?canceled=true',
                )
                return Response({'url': checkout_session.url})
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)
