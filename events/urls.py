from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

# router.register('event', views.EventViewset, basename='event')
router.register('', views.EventGenericViewSet, basename='')
# router.register('upsert', views.EventGenericPostViewSet, basename='upsert')

urlpatterns = [
    path('', include(router.urls)),
    # path('viewset/<str:pk>/', include(router.urls)),

    # path('', views.EventAPIView.as_view()),
    # path('create/', views.EventPostView.as_view()),
    # path('<str:event_id>/', views.EventDetails.as_view()),
    # path('update-delete/', views.EventDetailsPutDeleteView.as_view()),
    # path('generic/', views.EventGenericAPIView.as_view()),
]