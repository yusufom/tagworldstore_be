from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product, WishList, ProductReview
from products.serializers import CreateReviewSerializer, ProductSerializer, ReviewSerializer, WishListSerializer 
from rest_framework import status
# Create your views here.
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny

class ProductListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = Product.objects.prefetch_related("variation", "image")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductSingleView(APIView):
    permission_classes = [AllowAny]
    
    
    def get(self, request, slug):
        try:
            products = Product.objects.get(slug=slug)
            serializer = ProductSerializer(products)
            return Response(serializer.data)
        except Exception as e:
            return Response(data={"error": str(e)})
        
        
class WishListApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        print(request.user)
        user = request.user
        try:
            pass
        except Exception as e:
            return Response(data={"error m": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        product = Product.objects.get(id=request.data['product'])
        wishlist = WishList.objects.filter(user=request.user).first()
        if wishlist:
            wishlist.product.add(product)
            wishlist.save()
        else:
            wishlist = WishList.objects.create(user=request.user)
            wishlist.product.add(product)
            wishlist.save()
            
        return Response(data={"message": "Product added to wishlist"})
    
    def put(self, request):
        product = Product.objects.get(id=request.data['product'])
        wishlist = WishList.objects.filter(user=request.user).first()
        if wishlist:
            wishlist.product.remove(product)
            wishlist.save()
            
        return Response(data={"message": "Product added to wishlist"})

class GetProductReviewtView(APIView):
    permission_classes = [AllowAny]
    
    
    def get(self, request, id):
        try:
            product_id = Product.objects.get(id=id)
            review = ProductReview.objects.filter(product=product_id, approved=True)
            serializer = ReviewSerializer(review, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(data={"error": str(e)})

class ProductReviewtView(APIView):
    permission_classes = [IsAuthenticated]
        
    def post(self, request):
        serializer = CreateReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
            
        return Response(data={"message": "Review has been successfully added"})