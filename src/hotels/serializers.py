from rest_framework import serializers

from .models import Facilities, Hotels, Rooms


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


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        exclude = ["hotel"]


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = "__all__"
