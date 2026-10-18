from django.urls import path

from hotels.views import (
    FacilityListCreateAPIView,
    FacilityUpdateDeletePIView,
    HotelDetailAPIView,
    HotelListCreateAPIView,
    RoomDeleteAPIView,
    RoomListCreateAPIView,
)

urlpatterns = [
    path("", HotelListCreateAPIView.as_view()),
    path("facilities/", FacilityListCreateAPIView.as_view()),
    path("facilities/<int:pk>/", FacilityUpdateDeletePIView.as_view()),
    path("<int:hotel_id>/", HotelDetailAPIView.as_view()),
    path("<int:hotel_id>/room/", RoomListCreateAPIView.as_view()),
    path("<int:hotel_id>/room/<int:room_id>/", RoomDeleteAPIView.as_view()),
]
