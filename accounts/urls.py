from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

router.register('', views.AccountViewSet, basename='register')
router.register('verify-email', views.VerifyEmail, basename='verify-email')
# router.register('list', views.GetAllAccountViewSet, basename='list')
print("router >>>", router.get_urls())
urlpatterns = [
    path('', include(router.urls)),
]