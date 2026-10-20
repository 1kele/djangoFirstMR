from rest_framework import serializers

from bookings.models import Bookings


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = "__all__"


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ["id", "room", "start_date", "end_date"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["start_date"] >= attrs["end_date"]:
            raise serializers.ValidationError("Дата заселения не может быть позже даты выезда")

        return attrs
