from django.shortcuts import render
from rest_framework_simplejwt.jwt_views import TokenObtainPairView

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer