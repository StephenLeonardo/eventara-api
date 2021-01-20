from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('', views.CategoryView, basename='')

urlpatterns = [
    path('', include(router.urls)),
#     path('', views.CategoryAPIView.as_view()),
#     path('<str:id>/', views.CategoryDetails.as_view()),
]


