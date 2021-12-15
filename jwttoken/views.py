from django.db.models.query_utils import Q
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Account
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        
        if ('email' in request.data and 'password' in request.data):
            email = request.data.get('email', '')
            password = request.data.get('password', '')
            try:
                account = Account.objects.get((Q(username=email) | Q(email=email))
                                                & Q(is_active=True))

                if account.is_verified:
                    if account.check_password(password):
                        refresh = RefreshToken.for_user(account)

                        token = {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh)
                        }

                        return Response({
                            'Status': True,
                            'Message': 'Wow it worked!',
                            'Data': token
                        })
                    else:
                        return Response({
                            'Status': False,
                            'Message': 'Email or Password is incorrect'
                        }, status=status.HTTP_401_UNAUTHORIZED)
            except Account.DoesNotExist:
                return Response({
                    'Status': False,
                    'Message': 'Email or Password is incorrect.'
                }, status=status.HTTP_401_UNAUTHORIZED)


            return Response({
                'Status': False,
                'Message': 'Email has not yet been verified, please check your email'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
        return Response({
            'Status': False,
            'Message': 'email and password is required'
        }, status=status.HTTP_400_BAD_REQUEST)