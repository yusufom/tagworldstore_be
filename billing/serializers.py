from rest_framework import serializers
from .models import BillingAddress

class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}, 
        }

    def create(self, validated_data):
        user = self.context['request'].user
        billing_address = BillingAddress.objects.create(user=user, **validated_data)
        return billing_address
