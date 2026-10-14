from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Hotels
from hotels.serializers import HotelSerializer


class HotelsAPIView(APIView):
    def get(self, request):
        hotels = Hotels.objects.all()

        serializer = HotelSerializer(hotels)

        return Response(serializer.data)
