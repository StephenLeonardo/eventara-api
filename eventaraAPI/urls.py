"""eventaraAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from jwttoken.views import MyTokenObtainPairView


schema_view = get_schema_view(
    openapi.Info(
        title="EVENT API",
        default_version="v1",
        description="This API is for get, create, update, delete, etc",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="stephenleonardo18@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/', include('events.urls')),
    path('category/', include('categories.urls')),
    path('account/', include('accounts.urls')),
    
    
    
    path('api/token/', MyTokenObtainPairView.as_view(),
            name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
            name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
