from rest_framework import generics, status
from rest_framework.response import Response

from bookings.models import Bookings
from bookings.serializer import BookingCreateSerializer, BookingSerializer
from bookings.services import add_new_booking, update_booking


class BookingCreateListAPIView(generics.ListCreateAPIView):
    queryset = Bookings.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookingCreateSerializer

        return BookingSerializer

    def perform_create(self, serializer):
        booking_data = add_new_booking(serializer.validated_data)

        serializer.save(**booking_data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({"id": response.data["id"]}, status=status.HTTP_201_CREATED)


class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer

    def perform_update(self, serializer):
        if serializer.instance.is_actual_sensitive_changes(serializer.validated_data):
            booking_data = update_booking(serializer.instance, serializer.validated_data)
            serializer.save(**booking_data)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return Response({"id": response.data["id"]}, status=status.HTTP_200_OK)


class BookingFromRoomAPIView(generics.ListAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer

    lookup_field = "room"
    lookup_url_kwarg = "room_id"

    def get_queryset(self):
        return Bookings.objects.filter(room=self.kwargs["room_id"])
