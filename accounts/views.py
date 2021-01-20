from django.shortcuts import render
# from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, AccountSerializer
from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
import json
from django.forms.models import model_to_dict
from rest_framework.settings import api_settings
from .models import Account

# Create your views here.
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
    
class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RegisterSerializer
    
    
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AccountSerializer
        if self.action == 'create':
            return RegisterSerializer
    
    def get_queryset(self):
        queryset = Account.objects.all()
        
        
    def list(self, request):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        
        list_accounts = Account.objects.all()        
        accounts = paginator.paginate_queryset(list_accounts, request)
        serializer = AccountSerializer(accounts, many=True)
        
        return Response({
            'Status': 'Success',
            'Message': 'Wow it worked!',
            'Data': paginator.get_paginated_response(serializer.data).data
        })
        
        return Response(account_serializer.data)
    
    
    def create(self, request):
        current_serializer = self.get_serializer_class()
        serializer = current_serializer(data=request.data)
        print(request.data)
        
        if serializer.is_valid():
            account = Account.objects.create_user(**serializer.validated_data)
            print(model_to_dict(account))
            get_serializer = AccountSerializer(instance=account)
            
            
            return Response({
                'Status': 'Success',
                'Message': 'Wow it worked!',
                'Data': get_serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
