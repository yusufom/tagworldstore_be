from rest_framework import serializers

from products.models import Image, Product, Variation


class VariationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Variation
        exclude = ["products"]
        depth = 1

class ImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        exclude = ["products", "id"]
        depth = 1

class ProductSerializer(serializers.ModelSerializer):
    variation = VariationSerializer(many=True)
    image = ImagesSerializer(many=True)
    tag = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = "__all__"
        depth = 2
        
    def get_tag(self, obj):
        return [tag.name for tag in obj.tag.all()]
    
    def get_category(self, obj):
        return [cat.name for cat in obj.category.all()]