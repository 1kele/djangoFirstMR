from django.urls import path

from hotels.views import (
    FacilitiesListCreateAPIView,
    FacilitiesUpdateDeletePIView,
    HotelAPIView,
    RoomDeleteAPIView,
    RoomListCreateAPIView,
)

urlpatterns = [
    path("", HotelAPIView.as_view()),
    path("facilities/", FacilitiesListCreateAPIView.as_view()),
    path("facilities/<int:pk>/", FacilitiesUpdateDeletePIView.as_view()),
    path("<int:hotel_id>/", HotelAPIView.as_view()),
    path("<int:hotel_id>/room/", RoomListCreateAPIView.as_view()),
    path("<int:hotel_id>/room/<int:room_id>/", RoomDeleteAPIView.as_view()),
]
