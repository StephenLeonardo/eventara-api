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
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.decorators import action
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
    
class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [AllowAny]
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
            'Status': True,
            'Message': 'Wow it worked!',
            'Data': paginator.get_paginated_response(serializer.data).data
        })
        
        return Response(account_serializer.data)
    
    
    def create(self, request):
        current_serializer = self.get_serializer_class()
        serializer = current_serializer(data=request.data)
        
        if serializer.is_valid():
            account = Account.objects.create_user(**serializer.validated_data)
            get_serializer = AccountSerializer(account)
            
            
            token = RefreshToken.for_user(account).access_token
            
            current_site = get_current_site(request).domain
            relative_link = reverse('verify-email-verify')
            abs_url = request.is_secure() and "https" or "http" + '://'+current_site+relative_link+"?token="+str(token)
            email_body = 'Hi {}. Use the link below to verify your email:\n{}'.format(account.username, abs_url)
                        
            data = {
                'email_body': email_body,
                'email_subject': 'Evehunt - Verify your Email',
                'email_to': account.email
            }
            
            Util.send_verification_email(data)
            
            
            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': get_serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])    
    def log_in(self, request, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        
        try:            
            account = Account.objects.get((Q(username=email) | Q(email=email))
                                        & Q(is_active=True))
                                        
            if account.is_email_verified:
                if account.check_password(password):
                    get_serializer = AccountSerializer(account)
                    return Response({
                        'Status': True,
                        'Message': 'Wow it worked!',
                        'Data': get_serializer.data,
                    })
                else:
                    return Response({
                        'Status': False,
                        'Message': 'Email or Password is incorrect'
                    })
            else:
                token = RefreshToken.for_user(account).access_token
                
                current_site = get_current_site(request).domain
                relative_link = reverse('verify-email-verify')
                abs_url = request.is_secure() and "https" or "http" + '://'+current_site+relative_link+"?token="+str(token)
                email_body = 'Hi {}. Use the link below to verify your email:\n{}'.format(account.username, abs_url)
                            
                data = {
                    'email_body': email_body,
                    'email_subject': 'Evehunt - Verify your Email',
                    'email_to': account.email
                }
                
                Util.send_verification_email(data)
                
                
                return Response({
                    'Status': False,
                    'Message': 'We have sent an email to {}. Please verify your email before proceeding'.format(account.email)
                })                            
                                        
            
        except Account.DoesNotExist:
            return Response({
                'Status': False,
                'Message': 'Email or Password is incorrect'
            })
            
        
        
        
class VerifyEmail(viewsets.GenericViewSet):
    
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                         description='Description', type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config], method='GET')
    @action(methods=['GET'], detail=False)
    def verify(self, request):
        token = request.query_params.get('token', None)
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY).decode("utf-8")
            print(payload)
            account = Account.objects.get(id=payload['user_id'])
            if not account.is_email_verified:
                account.is_email_verified = True
            account.save()
            
            result_serializer = AccountSerializer(account)
            return Response({
                'Status': True,
                'Message': 'Congratulations, your email has been verified!',
                'Data': result_serializer.data
            })
            
        except jwt.ExpiredSignatureError as ex:
            return Response({
                'Status': False,
                'Message': 'Activation Expired'
            })
        
        except jwt.exceptions.DecodeError as ex:
            return Response({
                'Status': False,
                'Message': 'Invalid Token!'
            })
        
        except Account.DoesNotExist:
            return Response({
                'Status': False,
                'Message': 'Email or Password is incorrect'
            })
        
        
        
        
        
        
    
