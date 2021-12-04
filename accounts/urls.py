from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# router.register('', views.AccountViewSet.as_view({'get': 'account'}), basename="account"),
router.register('', views.AccountViewSet, basename='account')
# router.register('email-verification', views.EmailVerificationViewSet, basename='email-verification')
router.register('organization-verification', views.OrganizationVerificationViewSet,
                    basename='organization-verification')
router.register('verify-email-backdoor', views.VerifyEmailBackDoor,
                    basename='verify-email-backdoor')


urlpatterns = [
    path('', include(router.urls)),
    # path('', views.AccountViewSet.as_view({'get':'account', }), name="account"),
]

# urlpatterns += router.urls