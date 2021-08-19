from django.shortcuts import render
# from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (RegisterSerializer, AccountSerializer,
                            LoginSerializer, RequestVerifSerializer,
                            LoginReturnSerializer, EmailVerifSerializer,
                            OrganizationVerifSerializer)
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# import json
# from django.forms.models import model_to_dict
from rest_framework.settings import api_settings
from .models import Account
# from django.contrib.auth.hashers import check_password
from django.db.models import Q
# from .utils import Util
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
from rest_framework.decorators import action
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# import base64




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



    def create(self, request):
        '''
        Register account
        '''
        current_serializer = self.get_serializer_class()
        serializer = current_serializer(data=request.data)

        if serializer.is_valid():
            account = Account.objects.create_user(**serializer.validated_data)
            get_serializer = AccountSerializer(account)


            # token = RefreshToken.for_user(account).access_token

            # current_site = get_current_site(request).domain
            # relative_link = reverse('verify-email-verify')
            # abs_url = request.is_secure() and "https" or "http" + '://'+current_site+relative_link+"?token="+str(token)
            # email_body = 'Hi {}. Use the link below to verify your email:\n{}'.format(account.username, abs_url)

            # data = {
            #     'email_body': email_body,
            #     'email_subject': 'Evehunt - Verify your Email',
            #     'email_to': account.email
            # }

            # Util.send_verification_email(data)


            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': get_serializer.data,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(request_body=LoginSerializer, method='POST',
                operation_description="Log in with username/email and password")
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
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # token = RefreshToken.for_user(account).access_token

                # current_site = get_current_site(request).domain
                # relative_link = reverse('verify-email-verify')
                # abs_url = request.is_secure() and "https" or "http" + '://'+current_site+relative_link+"?token="+str(token)
                # email_body = 'Hi {}. Use the link below to verify your email:\n{}'.format(account.username, abs_url)

                # data = {
                #     'email_body': email_body,
                #     'email_subject': 'Evehunt - Verify your Email',
                #     'email_to': account.email
                # }

                # Util.send_verification_email(data)


                return Response({
                    'Status': False,
                    'Message': 'Email has not yet been verify, please check your email'
                }, status=status.HTTP_401_UNAUTHORIZED)


        except Account.DoesNotExist:
            return Response({
                'Status': False,
                'Message': 'Email or Password is incorrect'
            })


    @swagger_auto_schema(request_body=RequestVerifSerializer, method='POST',
                operation_description="Request organizer verif, it will send email to admin")
    @action(methods=['POST'], detail=False,
                permission_classes=[IsAuthenticatedOrReadOnly])
    def request_organization_verification(self, request):
        serializer = RequestVerifSerializer(data=request.data)

        if serializer.is_valid():
            account_id = serializer.data.get('account_id', None)

            try:
                account = Account.objects.get(id=account_id)

                # current_site = get_current_site(request).domain
                # relative_link = reverse('verify-organization-verify')

                # message_bytes = account.email.encode('ascii')
                # email_bytes = base64.b64encode(message_bytes)
                # email_enc = email_bytes.decode('ascii')

                # abs_url = request.is_secure() and "https" or "http" + '://'+current_site+relative_link+"?email="+str(email_enc)
                # email_body = '''
                # Account name : {username}\n



                # Use the link below to verify their organization:\n
                # {url}
                # '''.format(
                #     username=account.username,
                #     email=account.email,
                #     url=abs_url
                # )

                # data = {
                #     'email_body': email_body,
                #     'email_subject': 'Evehunt - Request Organization Verification',
                #     'email_to': settings.ADMIN_EMAIL
                # }

                # Util.send_verification_email(data)

                return Response({
                    'Status': True,
                    'Message': '''Email request for verification has been sent!
                               Please wait to be informed
                               '''
                })

            except Account.DoesNotExist:
                return Response({
                    'Status': False,
                    'Message': 'Account not found!'
                }, status=status.HTTP_404_NOT_FOUND)




class VerifyEmail(viewsets.GenericViewSet):

    serializer_class = EmailVerifSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                         description='Description', type=openapi.TYPE_STRING,
                         required=True)

    @swagger_auto_schema(manual_parameters=[token_param_config], method='POST')
    @action(methods=['POST'], detail=False)
    def verify(self, request):
        token = request.data.get('token', None)
        try:
            payload =   jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
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


class VerifyOrganization(viewsets.GenericViewSet):

    serializer_class = OrganizationVerifSerializer

    email_param_config = openapi.Parameter('email', in_=openapi.IN_QUERY,
                         description='email', type=openapi.TYPE_STRING,
                         required=True)


    @swagger_auto_schema(method='POST', manual_parameters=[email_param_config])
    @action(methods=['POST'], detail=False)
    def verify(self, request):

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


class VerifyEmailBackDoor(viewsets.GenericViewSet):
    serializer_class = OrganizationVerifSerializer


    @swagger_auto_schema(method='POST')
    @action(methods=['POST'], detail=False)
    def verify(self, request):
        try:
            email = request.data.get('email',None)
            account = Account.objects.get(email=email)

            if not account.is_verified:
                account.is_verified = True
            if not account.is_email_verified:
                account.is_email_verified = True

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