from django.urls import path
from .views import WeatherTodayView, WeatherTomorrowView

urlpatterns = [
    path('weather/today/', WeatherTodayView.as_view()),
    path('weather/tomorrow/', WeatherTomorrowView.as_view()),
]