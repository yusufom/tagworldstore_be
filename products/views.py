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
        
        
class GetAllWishListApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            wishlist = WishList.objects.filter(user=user).first()
            if wishlist:
                serializer = ProductSerializer(wishlist.product.all(), many=True)
                return Response(serializer.data)
            else:
                wishlist_create = WishList.objects.create(user=request.user)
                wishlist_create.save()
                serializer = ProductSerializer(wishlist_create.product.all(), many=True)
                return Response(serializer.data)
        except Exception as e:
            return Response(data={"error m": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class CreateWishListApiView(APIView):
    permission_classes = [IsAuthenticated]
    
        
    def post(self, request):
        try:
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
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UpdateWishListApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def put(self, request):
        try:
            product = Product.objects.get(id=request.data['product'])
            wishlist = WishList.objects.filter(user=request.user).first()
            if wishlist:
                wishlist.product.remove(product)
                wishlist.save()
                
            return Response(data={"message": "Product added to wishlist"})
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ClearWishListApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def put(self, request):
        try:
            wishlist = WishList.objects.filter(user=request.user).first()
            if wishlist:
                wishlist.delete()
                
            return Response(data={"message": "Wishlist cleared successfully"})
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        print()
        serializer = CreateReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data={"message": "Review has been successfully added"})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)