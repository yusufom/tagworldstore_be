from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BillingAddress
from .serializers import BillingAddressSerializer
from rest_framework.permissions import IsAuthenticated


class BillingAddressListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = BillingAddress.objects.filter(user=request.user)
        serializer = BillingAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BillingAddressSerializer(data=request.data, context={'request': request})
        # print(serializer)
        # print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillingAddressDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(BillingAddress, pk=pk, user=self.request.user)

    def get(self, request, pk):
        address = self.get_object(pk)
        serializer = BillingAddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = self.get_object(pk)
        serializer = BillingAddressSerializer(
            address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)