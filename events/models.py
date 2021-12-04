from django.db import models
import uuid
from django.utils.http import int_to_base36
from django.utils.crypto import get_random_string

from categories.models import Category
from organizers.models import Organizer
from accounts.models import Account
import datetime

def id_gen():
    """Generates random string whose length is `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:6]


# class EventImage(models.Model):
#     event_image_id = models.CharField(max_length=gu)

#     class Meta:
#         db_table = "EventImages"

def get_current_month_year():
    return '{}-{}'.format(datetime.datetime.now().month, datetime.datetime.now().year)


def path_and_rename(instance, filename):
    upload_to = 'events/{}/'.format(get_current_month_year())
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    if instance.pk:
        filename = '{}_{}.{}'.format(now.strftime('%d%H%M%S'), str(instance.pk)[:5], ext)
    else:
        allowed_chars=u'abcdefghijklmnopqrstuvwxyz0123456789'
        filename = '{}_{}.{}'.format(now.strftime('%d%H%M%S'), get_random_string(length=5, allowed_chars=allowed_chars), ext)
    return '{}{}'.format(upload_to, filename)

# Create your models here.
class Event(models.Model):
    event_id = models.CharField(max_length=6, primary_key=True, default=id_gen, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=None, null=True, blank=True)
    image = models.URLField(null=True, blank=True, max_length=255)
    organizer = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255)
    event_date = models.DateField(blank=True, null=True)
    event_start_time = models.TimeField(blank=True, null=True)
    event_end_time = models.TimeField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    is_online = models.BooleanField(default=False)
    registration_link = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



    @property
    def thumbnail(self):
        return self.event_images.first()


    def __str__(self):
        return self.name

    class Meta:
        db_table = "Events"


class EventImage(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    image = models.URLField(null=True, blank=True, max_length=255)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    dominant_color = models.CharField(max_length=50, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image_order = models.IntegerField()

    def __str__(self):
        return self.image_url

    class Meta:
        db_table = "EventImages"
