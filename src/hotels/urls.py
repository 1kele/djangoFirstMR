from django.urls import path

from hotels.views import HotelsAPIView

urlpatterns = [
    path("", HotelsAPIView.as_view()),
    path("<int:pk>/", HotelsAPIView.as_view()),
]
