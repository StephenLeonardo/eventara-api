from django.urls import path
from . import views


urlpatterns = [
    path('', views.CategoryAPIView.as_view()),
    path('<str:id>/', views.CategoryDetails.as_view()),
]