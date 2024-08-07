from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from products.models import Product, Size, Variation
from .models import CartItem, Order
from billing.models import BillingAddress
from .serializers import CartItemSerializer, CartItemListSerializer, CheckoutSessionSerializer, ConfirmOrderSerializer, CreateMulitpleCartItemsSerializer, ListOrderSerializer, OrderSerializer
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
import os
from dotenv import load_dotenv

load_dotenv()


import stripe

stripe.api_key = os.environ.get('STRIPE_API_KEY')
YOUR_DOMAIN = os.environ.get('YOUR_DOMAIN')

class CreateCartMultiple(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        serializer = CreateMulitpleCartItemsSerializer(data=request.data)
        if serializer.is_valid():
            items = serializer.validated_data.get('items')
            for item in items:
                product_data = item.get('product')
                product = Product.objects.get(id=product_data["id"])
                cart_item_filter = CartItem.objects.filter(
                    user=user,
                    product=product,
                    selected_product_color=item.get('selected_product_color'),
                    selected_product_size=item.get('selected_product_size'),
                    ordered=False
                ).first()
                if cart_item_filter:
                    cart_item_filter.quantity += item.get('quantity')
                    cart_item_filter.save()
                else:
                    cart_item = CartItem.objects.create(
                        user=user,
                        product=product,
                        selected_product_color=item.get('selected_product_color'),
                        selected_product_size=item.get('selected_product_size'),
                        quantity=item.get('quantity'),
                        ordered=False
                    )
                    cart_item.save()
                    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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
                size = variation.size.get(name=request.data.get('selected_product_size'))
            except Variation.DoesNotExist:
                pass
            except Size.DoesNotExist:
                pass
            except Exception: 
                pass
            
            res = serializer.validated_data
            res["product"].update(image=image)
            cart_item = CartItem.objects.filter(
                user=user,
                product=product,
                selected_product_color=request.data.get('selected_product_color'),
                selected_product_size=request.data.get('selected_product_size'),
                ordered=False
            ).first()
            

            if cart_item:
                
                cart_item.quantity += request.data.get('quantity', 1)
                if cart_item.quantity > cart_item.product.stock:
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
        # print("data here",request.data)
        serializer = CheckoutSessionSerializer(data=request.data)
        if serializer.is_valid():
            pkid = serializer.validated_data['pkid']
            b_id = serializer.validated_data['address']
            
            try:
                address = BillingAddress.objects.get(pk=b_id)
                order = Order.objects.get(pkid=pkid)
                order.ordered = True
                order.note = request.data.get('note', '')
                order.shipping_address = address
                order.status = "Confirmed"
                order.save()
                checkout_session = stripe.checkout.Session.create(
                    line_items=serializer.validated_data['line_items'],
                    mode='payment',
                    success_url=YOUR_DOMAIN + '/?soc12sde=' + str(pkid) +'&success=true',
                    cancel_url=YOUR_DOMAIN + '/?soc12sde=' + str(pkid) + '&canceled=true',
                )
                return Response({'url': checkout_session.url})
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-ordered_date')
        serializer = ListOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        try:
            user = request.user
            serializer = OrderSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                print(serializer.validated_data['items'])
                order = Order.objects.create(user=user)
                for item in serializer.validated_data['items']:
                    cart_item = CartItem.objects.get(id=item['id'], user=user)
                    cart_item.ordered = True
                    order.items.add(cart_item)
                    cart_item.save()
                order.save()
                return Response({"pkid": order.pkid})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=False, methods=['put'])
    def update_order(self, request):
        print(request.data)
        try:
            user = request.user
            serializer = ConfirmOrderSerializer(data=request.data)
            
            if serializer.is_valid():
                order = Order.objects.get(user=user, pkid=serializer.validated_data['order_id'])
                if serializer.validated_data['status'] == "success":
                    order.is_paid = True
                    cart_items = CartItem.objects.filter(user=user, ordered=False)
                    for cart_item in cart_items:
                        cart_item.ordered = True
                        cart_item.save()
                    order.save()
                else:
                    order.is_paid = False
                    order.save()
                return Response({"message": "order successful"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
