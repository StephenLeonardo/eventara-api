from django.urls import path
from . import views


urlpatterns = [
    path('', views.EventAPIView.as_view()),
    path('<str:event_id>/', views.EventDetails.as_view()),
]