from rest_framework import generics

from bookings.models import Bookings
from bookings.serializer import BookingCreateSerializer, BookingSerializer
from services import add_new_booking


class BookingCreateListAPIView(generics.ListCreateAPIView):
    queryset = Bookings.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookingCreateSerializer

        return BookingSerializer

    def perform_create(self, serializer):
        booking_data = add_new_booking(serializer.validated_data)

        serializer.save(**booking_data)


class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer


class BookingFromRoomAPIView(generics.ListAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer

    lookup_field = "room"
    lookup_url_kwarg = "room_id"

    def get_queryset(self):
        return Bookings.objects.filter(room=self.kwargs["room_id"])
