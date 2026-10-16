from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Hotels, Rooms
from hotels.serializers import HotelFilterSerializer, HotelSerializer, RoomSerializer


class HotelsAPIView(APIView):
    def get(self, request):
        serializer_filters = HotelFilterSerializer(data=request.query_params)
        serializer_filters.is_valid(raise_exception=True)

        filters = serializer_filters.validated_data

        hotel = Hotels.objects.filter(**filters)

        serializer = HotelSerializer(hotel, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        hotel = get_object_or_404(Hotels, pk=pk)
        serializer = HotelSerializer(
            hotel,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        hotel = get_object_or_404(Hotels, pk=pk)
        serializer = HotelSerializer(hotel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        hotel = get_object_or_404(Hotels, pk=pk)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        return Rooms.objects.filter(hotel_id=self.kwargs["hotel_id"])

    def perform_create(self, serializer):
        pk = self.kwargs.get("hotel_id")
        serializer.save(hotel_id=pk)


class RoomDeleteAPIView(generics.DestroyAPIView):
    queryset = Rooms.objects.all()

    lookup_field = "id"
    lookup_url_kwarg = "room_id"

    def get_queryset(self):
        return Rooms.objects.filter(hotel_id=self.kwargs["hotel_id"])
