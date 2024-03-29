from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import json
from organizers.serializers import OrganizationSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass

        try:
            request_data = json.loads(request.body)
            if("username" in request_data and "password" in request_data):
                # default scenario in simple-jwt
                pass

            else:
                # some fields were missing
                raise serializers.ValidationError({"username/otp or username/password" : "These fields are required"})

        except:
            pass


from rest_framework import serializers
from .models import Account, Subscription




class AccountSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    class Meta:
        model = Account
        fields = ['id',
                'username',
                'profile_picture',
                'description',
                'location',
                'is_verified',
                'is_organizer',
                'organization',
                'is_staff']

class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class LoginTokenSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    # token = TokenSerializer()
    class Meta:
        model = Account
        fields = ['account',
                # 'token'
                ]

class AccountPostSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    class Meta:
        model = Account
        fields = [
                'username',
                'location',
                'password',
                'profile_picture',
                'description',]




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username',
                'email',
                'password',
                'profile_picture',
                'description',]

class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    

class RequestVerifSerializer(serializers.Serializer):
    account_id = serializers.CharField()


class LoginReturnSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()

    @classmethod
    def get_token(self, account):
        refresh = RefreshToken.for_user(account)
        token = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        return token

    @classmethod
    def get_account(self, account):
        return AccountSerializer(account).data

    class Meta:
        model = Account
        fields = ['account',
                'token',
                ]

class EmailVerifSerializer(serializers.Serializer):
    token = serializers.CharField()

class OrganizationVerifSerializer(serializers.Serializer):
    email = serializers.CharField()


class SubscriptionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        exclude = ('created_date', 'updated_date')