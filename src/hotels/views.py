from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Hotels
from hotels.serializers import HotelFilterSerializer, HotelSerializer


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
