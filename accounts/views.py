from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.models import Profile
from accounts.serializers import ProfileSerializer
# Create your views here.
class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(instance=profile)
            return Response(serializer.data)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(instance=profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"message": "Profile Updated successfully"})
            return Response(serializer.errors)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)