from rest_framework import generics, mixins, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Facilities, Hotels, Rooms
from hotels.serializers import (
    FacilitiesSerializer,
    HotelFilterSerializer,
    HotelSerializer,
    RoomSerializer,
)


class HotelListCreateAPIView(APIView):
    def get(self, request):
        hotels = Hotels.objects.all()
        serializer = HotelSerializer(hotels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HotelDetailAPIView(APIView):
    def get(self, request, hotel_id):
        serializer_filters = HotelFilterSerializer(data=request.query_params)
        serializer_filters.is_valid(raise_exception=True)

        filters = serializer_filters.validated_data

        hotel = Hotels.objects.filter(**filters, id=hotel_id)

        serializer = HotelSerializer(hotel, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, hotel_id):
        hotel = get_object_or_404(Hotels, pk=hotel_id)
        serializer = HotelSerializer(
            hotel,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, hotel_id):
        hotel = get_object_or_404(Hotels, pk=hotel_id)
        serializer = HotelSerializer(hotel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, hotel_id):
        hotel = get_object_or_404(Hotels, pk=hotel_id)
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({"id": serializer.instance.id}, status=status.HTTP_201_CREATED)


class RoomDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer

    lookup_field = "id"
    lookup_url_kwarg = "room_id"

    def get_queryset(self):
        return Rooms.objects.filter(hotel_id=self.kwargs["hotel_id"])


class FacilityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Facilities.objects.all()
    serializer_class = FacilitiesSerializer


class FacilityUpdateDeletePIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView
):
    queryset = Facilities.objects.all()
    serializer_class = FacilitiesSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
