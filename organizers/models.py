from django.db import models

import uuid
from django.utils.http import int_to_base36

def id_gen():
    """Generates random string whose length is `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:6]

# Create your models here.
class Organizer(models.Model):
    organizer_id = models.CharField(max_length=10, primary_key=True, default=id_gen, editable=False)
    name = models.CharField(max_length=255)
    photo = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = "organizers"