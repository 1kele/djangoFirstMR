from rest_framework import serializers

from .models import Hotels


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotels
        fields = "__all__"


class HotelFilterSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    founding_date = serializers.DateField(required=False)
    stars = serializers.IntegerField(required=False)
