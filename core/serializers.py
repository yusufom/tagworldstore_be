from rest_framework import serializers
from core.models import Slide
class SlideSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Slide
        fields = "__all__"
        depth = 1