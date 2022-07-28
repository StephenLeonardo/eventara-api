from email.mime import base
from django.urls import path, include

from accounts.custom_router import CustomRouter
from . import views
from rest_framework.routers import DefaultRouter


router = CustomRouter()

router.register('', views.AccountViewSet, basename='account')
router.register('organization-verification', views.OrganizationVerificationViewSet,
                    basename='organization-verification')
router.register('verify-email-backdoor', views.VerifyEmailBackDoor,
                    basename='verify-email-backdoor')
router.register('subscription', views.SubscriptionViewSet,
                    basename='subscription')


urlpatterns = [
    path('', include(router.urls)),
    # path('', views.AccountViewSet.as_view({'get':'account', }), name="account"),
]

# urlpatterns += router.urls