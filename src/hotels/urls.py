from django.urls import path

from hotels.views import HotelsAPIView, RoomDeleteAPIView, RoomListCreateAPIView

urlpatterns = [
    path("", HotelsAPIView.as_view()),
    path("<int:hotel_id>/", HotelsAPIView.as_view()),
    path("<int:hotel_id>/room/", RoomListCreateAPIView.as_view()),
    path("<int:hotel_id>/room/<int:room_id>/", RoomDeleteAPIView.as_view()),
]
