from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from core.models import Slide
from core.serializers import SlideSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



# Create your views here.

class SlideView(APIView):
    permission_classes = [AllowAny]
    
    
    def get(self, request):
        try:
            slides = Slide.objects.filter(is_active=True)
            serializer = SlideSerializer(slides, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(data={"error": str(e)})