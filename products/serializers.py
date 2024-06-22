from rest_framework import serializers

from products.models import Image, Product, Variation, Size, WishList, ProductReview


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
    
class SizeCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"
class VariationCartSerializer(serializers.ModelSerializer):
    size = SizeCartSerializer(many=True)
    
    
    class Meta:
        model = Variation
        exclude = ["products", "image"]
        

class ImagesCartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        exclude = ["products", "id"]
        depth = 1
           
class ProductCartSerializer(serializers.ModelSerializer):
    variation = VariationCartSerializer(many=True)
    id = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    
    
    class Meta:
        model = Product
        exclude = ["category", "tag"]
        depth = 2
        
        
class WishListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = WishList
        fields = ["product"]
        depth = 1
        
        
class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductReview
        fields = "__all__"
        depth = 1
        
class CreateReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductReview
        exclude = ["user", "approved"]