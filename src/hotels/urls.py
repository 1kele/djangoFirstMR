from django.urls import path

from hotels.views import (
    FacilityListCreateAPIView,
    FacilityUpdateDeletePIView,
    HotelAPIView,
    RoomDeleteAPIView,
    RoomListCreateAPIView,
)

urlpatterns = [
    path("", HotelAPIView.as_view()),
    path("facilities/", FacilityListCreateAPIView.as_view()),
    path("facilities/<int:pk>/", FacilityUpdateDeletePIView.as_view()),
    path("<int:hotel_id>/", HotelAPIView.as_view()),
    path("<int:hotel_id>/room/", RoomListCreateAPIView.as_view()),
    path("<int:hotel_id>/room/<int:room_id>/", RoomDeleteAPIView.as_view()),
]
