from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer 
# Create your views here.

class ProductListView(APIView):
    
    
    def get(self, request):
        products = Product.objects.prefetch_related("variation", "image")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductSingleView(APIView):
    
    
    def get(self, request, slug):
        try:
            products = Product.objects.get(slug=slug)
            serializer = ProductSerializer(products)
            return Response(serializer.data)
        except Exception as e:
            return Response(data={"error": str(e)})
        