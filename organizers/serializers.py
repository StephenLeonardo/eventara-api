from rest_framework import serializers
from .models import Organizer


class OrganizerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organizer
            fields = ['organizer_id', 'name', 'photo', 'description']
            
            
class OrganizerPostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organizer
            fields = ['name', 'photo', 'description']