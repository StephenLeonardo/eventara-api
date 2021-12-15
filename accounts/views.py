from datetime import timedelta
from os import stat
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from rest_framework.decorators import action
from .serializers import (AccountPostSerializer, RegisterSerializer, AccountSerializer,
                            LoginSerializer,
                            LoginReturnSerializer, EmailVerifSerializer,
                            OrganizationVerifSerializer)
from rest_framework import serializers, status
from rest_framework.mixins import (DestroyModelMixin, UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Account
from django.db.models import Q
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from drf_yasg.utils import get_serializer_class, swagger_auto_schema
from drf_yasg import openapi
from django.template.loader import render_to_string



class AccountViewSet(DestroyModelMixin, GenericViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    
    def get_object(self):
        if (self.action == "update" or self.action == "delete" or self.action == "partial_update") and self.kwargs.get(self.lookup_url_kwarg) is None:  # Check if this is an update method to the list view, the URL kwargs for the lookup will not be populated
            user = self.request.user
            return user
        return super().get_object()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AccountSerializer
        elif self.action == 'create':
            return RegisterSerializer
        elif self.action == 'update':
            return AccountPostSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'organization_verification':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    # Not a list, instead just returns one user from JWT
    def list(self, request):
        serializer = self.get_serializer_class()
        try:            
            account = request.user
            ret_data = serializer(account).data
            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': ret_data
            })


        except Exception as ex:
            return Response({
                'Status': True,
                'Message': ex
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        '''
        Register account
        '''
        current_serializer = self.get_serializer_class()
        serializer = current_serializer(data=request.data)

        if serializer.is_valid():
            account = Account.objects.create_user(**serializer.validated_data)
            get_serializer = AccountSerializer(account)


            token = RefreshToken.for_user(account).access_token
            token.set_exp(lifetime=timedelta(days=10))
            abs_url = f'{settings.FRONTEND_URL}email-verification/?token={str(token)}'
            msg_html = render_to_string('verification_email_template.html', {'redirect_url': abs_url, 'username': account.username})
            data = {
                'email_body': msg_html,
                'email_subject': 'Eventara - Verify your Email',
                'email_to': [account.email]
            }
            Util.send_verification_email(data)

            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': get_serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        instance = request.user

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'profile_picture' in serializer.validated_data and not serializer.validated_data['profile_picture']:
            serializer.validated_data.pop('profile_picture')
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': AccountSerializer(instance).data}
            )

    @swagger_auto_schema(request_body=LoginSerializer, method='POST',
                operation_description="Log in with username/email and password")
    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def login(self, request, **kwargs):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email', None)
        password = request.data.get('password', None)


        try:
            account = Account.objects.get((Q(username=email) | Q(email=email))
                                        & Q(is_active=True))

            if account.is_verified:
                if account.check_password(password):
                    get_serializer = LoginReturnSerializer(account)

                    return Response({
                        'Status': True,
                        'Message': 'Wow it worked!',
                        'Data': get_serializer.data,
                    })
                else:
                    return Response({
                        'Status': False,
                        'Message': 'Email or Password is incorrect.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                token = RefreshToken.for_user(account).access_token
                token.set_exp(lifetime=timedelta(days=10))
                abs_url = f'{settings.FRONTEND_URL}email-verification/?token={str(token)}'
                msg_html = render_to_string('verification_email_template.html', {'redirect_url': abs_url, 'username': account.username})
                data = {
                    'email_body': msg_html,
                    'email_subject': 'Eventara - Verify your Email',
                    'email_to': [account.email]
                }
                Util.send_verification_email(data)


                return Response({
                    'Status': False,
                    'Message': 'Email has not yet been verified, please check your email.'
                }, status=status.HTTP_401_UNAUTHORIZED)


        except Account.DoesNotExist:
            return Response({
                'Status': False,
                'Message': 'Email or Password is incorrect.'
            }, status=status.HTTP_401_UNAUTHORIZED)


    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, description='generated token')
        }
    ), method='POST')
    @action(methods=['POST'], detail=False, url_path='email-verification')
    def email_verification(self, request):
        token = request.data.get('token', None)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            account = Account.objects.get(id=payload['user_id'])
            if not account.is_verified:
                account.is_verified = True
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
                'Message': 'Activation Expired.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError as ex:
            return Response({
                'Status': False,
                'Message': 'Invalid Token!'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Account.DoesNotExist:
            return Response({
                'Status': False,
                'Message': 'Account with this email does not exist.'
            }, status=status.HTTP_401_UNAUTHORIZED)


    @swagger_auto_schema(method='POST')
    @action(methods=['POST'], detail=False, url_path='organization-verification')
    def organization_verification(self, request):

        try:

            account = request.user

            if not account.is_verified:
                account.is_verified = True

            account.save()

            ret_serializer = AccountSerializer(account)

            return Response({
                'Status': True,
                'Message': 'Congratulations, your organization has been verified!',
                'Data': ret_serializer.data
            })


        except Exception as e:
            return Response({
                'Status': False,
                'Message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

class EmailVerificationViewSet(GenericViewSet):                     

    serializer_class = EmailVerifSerializer
    authentication_classes = [AllowAny]
    queryset = Account.objects.all()

    # token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
    #                      description='Description', type=openapi.TYPE_STRING,
    #                      required=True)
    # @swagger_auto_schema(manual_parameters=[token_param_config], method='POST')
    # @action(methods=['POST'], detail=False)
    def create(self, request):
        token = request.data.get('token', None)
        try:
            payload =   jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            account = Account.objects.get(id=payload['user_id'])
            if not account.is_verified:
                account.is_verified = True
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
                'Message': 'Activation Expired.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError as ex:
            return Response({
                'Status': False,
                'Message': 'Invalid Token!'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Account.DoesNotExist:
            return Response({
                'Status': False,
                'Message': 'Account with this email does not exist.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class OrganizationVerificationViewSet(
                                GenericViewSet):

    serializer_class = OrganizationVerifSerializer
    authentication_classes = [IsAuthenticatedOrReadOnly]

    # email_param_config = openapi.Parameter('email', in_=openapi.IN_QUERY,
    #                      description='email', type=openapi.TYPE_STRING,
    #                      required=True)


    # @swagger_auto_schema(method='POST', manual_parameters=[email_param_config])
    # @action(methods=['POST'], detail=False)
    def create(self, request):

        try:
            # email_enc = request.data.get('email', None)
            # base64_bytes = email_enc.encode('ascii')
            # email_bytes = base64.b64decode(base64_bytes)
            # email = email_bytes.decode('ascii')

            email = request.data.get('email', None)

            account = Account.objects.get(email=email)

            if not account.is_verified:
                account.is_verified = True

            account.save()

            ret_serializer = AccountSerializer(account)

            return Response({
                'Status': True,
                'Message': 'Congratulations, your organization has been verified!',
                'Data': ret_serializer.data
            })


        except Exception as e:
            return Response({
                'Status': False,
                'Message': str(e)
            })


class VerifyEmailBackDoor(GenericViewSet):
    serializer_class = OrganizationVerifSerializer


    @swagger_auto_schema(method='POST')
    @action(methods=['POST'], detail=False)
    def verify(self, request):
        try:
            email = request.data.get('email',None)
            account = Account.objects.get(email=email)

            if not account.is_verified:
                account.is_verified = True

            account.save()

            ret_serializer = AccountSerializer(account)

            return Response({
                'Status': True,
                'Message': 'Congratulations, your account has been verified!',
                'Data': ret_serializer.data
            })

        except Exception as e:
            return Response({
                'Status': False,
                'Message': str(e)
            })