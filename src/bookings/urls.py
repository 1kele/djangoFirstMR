from django.urls import path

from bookings.views import BookingCreateListAPIView, BookingDetailAPIView, BookingFromRoomAPIView

urlpatterns = [
    path("", BookingCreateListAPIView.as_view()),
    path("<int:pk>/", BookingDetailAPIView.as_view()),
    path("room/<int:room_id>/", BookingFromRoomAPIView.as_view()),
]
