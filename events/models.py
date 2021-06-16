from django.db import models
import uuid
from django.utils.http import int_to_base36

from categories.models import Category
from organizers.models import Organizer
from accounts.models import Account

def id_gen():
    """Generates random string whose length is `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:6]

# Create your models here.
class Event(models.Model):
    event_id = models.CharField(max_length=6, primary_key=True, default=id_gen, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=None, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    organizer = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255)
    event_date = models.DateField(blank=True, null=True)
    event_start_time = models.TimeField(blank=True, null=True)
    event_end_time = models.TimeField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    is_online = models.BooleanField(default=False)
    registration_link = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "events"
