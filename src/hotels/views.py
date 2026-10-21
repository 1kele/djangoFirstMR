from rest_framework import generics, mixins, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from config.logging_setup import setup_logging
from hotels.models import Facilities, Hotels, Rooms
from hotels.serializers import (
    FacilitiesSerializer,
    HotelFilterSerializer,
    HotelSerializer,
    RoomSerializer,
)

logger = setup_logging()


class HotelListCreateAPIView(APIView):
    def get(self, request):
        hotels = Hotels.objects.all()
        serializer = HotelSerializer(hotels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hotel = serializer.save()
        logger.info("Hotel created: hotel_id: {}, name: {}", hotel.id, hotel.name)

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
        hotel = serializer.save()
        logger.info("Hotel fully updated: hotel_id: {}, name: {}", hotel.id, hotel.name)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, hotel_id):
        hotel = get_object_or_404(Hotels, pk=hotel_id)
        serializer = HotelSerializer(hotel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        hotel = serializer.save()
        logger.info("Hotel updated: hotel_id: {}, name: {}", hotel.id, hotel.name)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, hotel_id):
        hotel = get_object_or_404(Hotels, pk=hotel_id)
        hotel_id = hotel.id
        hotel.delete()
        logger.info("Hotel deleted: hotel_id: {}", hotel_id)

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
        room = serializer.save(hotel_id=pk)
        logger.info("Room created: room_id: {}, hotel_id: {}", room.id, room.hotel_id)

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

    def perform_update(self, serializer):
        room = serializer.save()

        logger.info("Room updated: room_id: {}, hotel_id: {}", room.id, room.hotel_id)

    def perform_destroy(self, instance):
        room_id = instance.id
        hotel_id = instance.hotel_id

        instance.delete()

        logger.info("Room deleted: room_id: {}, hotel_id: {}", room_id, hotel_id)


class FacilityListCreateAPIView(generics.ListCreateAPIView):
    queryset = Facilities.objects.all()
    serializer_class = FacilitiesSerializer

    def perform_create(self, serializer):
        facility = serializer.save()

        logger.info("Facility created: id: {}, name: {}", facility.id, facility.name)


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

    def perform_update(self, serializer):
        facility = serializer.save()

        logger.info("Facility updated: facility_id: {}, name: {}", facility.id, facility.name)

    def perform_destroy(self, instance):
        facility_id = instance.id
        name = instance.name

        instance.delete()

        logger.info("Facility deleted: facility_id: {}, name: {}", facility_id, name)
