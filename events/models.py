from django.db import models
import uuid
from django.utils.http import int_to_base36

from categories.models import Category
# from organizers.models import Organizer
from accounts.models import Account

def id_gen():
    """Generates random string"""
    return int_to_base36(uuid.uuid4().int)[:6]


# Create your models here.
class Event(models.Model):
    event_id = models.CharField(max_length=6, primary_key=True, default=id_gen, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=None, null=True, blank=True)
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

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Events"



class EventImage(models.Model):
    event_image_id = models.CharField(max_length=36, default=uuid.uuid4, editable=False, primary_key=True)
    image_url = models.CharField(max_length=255, blank=False, null=False)
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.image_url
    class Meta:
        db_table = "EventImages"
