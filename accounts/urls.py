from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', views.AccountViewSet, basename='register')
# router.register('list', views.GetAllAccountViewSet, basename='list')

urlpatterns = [
    path('', include(router.urls)),
]