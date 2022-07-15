from datetime import datetime
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
import uuid
from django.utils.crypto import get_random_string
from django.utils.http import int_to_base36
import json
from django.core.exceptions import ValidationError
from organizers.models import Organization

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password, profile_picture, description):
        if username is None:
            raise TypeError('The field Username is required')
        if email is None:
            raise TypeError('The field Email is required')
        if password is None:
            raise TypeError('The field Password is required')
            
        user = self.model(username=username, email=self.normalize_email(email),
                            profile_picture=profile_picture,
                            description=description)
        user.set_password(password)
        user.save()
    
        
        return user
    
    def create_superuser(self, username, email, password):
        if username is None:
            raise TypeError('The field Username is required')
        if email is None:
            raise TypeError('The field Email is required')
        if password is None:
            raise TypeError('The field Password is required')
        
        user = self.create_user(username, email, password)
        user.is_verified = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


def id_gen():
    """Generates random string whose length is `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:10]

def path_and_rename(instance, filename):
        ext = 'webp'
        now = datetime.now()
        if instance.pk:
            filename = '{}{}.{}'.format(now.strftime('%d%H%M%S'), str(instance.pk), ext)
        else:
            allowed_chars=u'abcdefghijklmnopqrstuvwxyz0123456789'
            filename = '{}{}.{}'.format(now.strftime('%d%H%M%S'), get_random_string(length=5, allowed_chars=allowed_chars), ext)
        return 'accounts/{}/{}'.format(now.strftime('%m-%Y'), filename)
        
class Account(AbstractBaseUser, PermissionsMixin):

    def validate_image(file):
        filesize = file.size
        megabyte_limit = 3.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    id = models.CharField(max_length=10, primary_key=True,
                                    default=id_gen, editable=False)
    username = models.CharField(max_length=100, unique=True, error_messages={
        'unique': 'Account with this username already exists.'
    })
    email = models.EmailField(max_length=255, unique=True, error_messages={
        'unique': 'Account with this email already exists.'
    })
    password = models.CharField(max_length=255)
    description = models.TextField(max_length=None, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True, validators=[validate_image])
    location = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
        
    def tokens(self):
        return ''
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
    class Meta:
        db_table = 'Accounts'




###########################################################################
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q

MyUser = get_user_model()

class UsernameOrEmailBackend(object):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
           # Try to fetch the user by searching the username or email field
            user = MyUser.objects.get((Q(username=email)|Q(email=email)) & Q(is_active=True))
            if user.check_password(password):
                return user
        except MyUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            MyUser().set_password(password)
            
    
    def get_user(self, id):
        MyUser = get_user_model()
        try:
            return MyUser.objects.get(pk=id)
        except MyUser.DoesNotExist:
            return None


class OrganizationRequest(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='organization_request')
    verified_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='organization_verified_by')
    verified_date = models.DateTimeField(null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        