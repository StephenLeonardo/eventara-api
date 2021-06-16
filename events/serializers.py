from rest_framework import serializers
from .models import Event

from categories.serializers import CategorySerializer
from organizers.serializers import OrganizerSerializer
from accounts.serializers import AccountSerializer


class EventSerializer(serializers.ModelSerializer):
    organizer = AccountSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Event
        fields = ['event_id',
                    'name',
                    'description',
                    'image',
                    'organizer',
                    'location',
                    'event_date',
                    'event_start_time',
                    'event_end_time',
                    'categories',
                    'is_online',
                    'registration_link']


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name',
                    'description',
                    'image',
                    'organizer',
                    'location',
                    'event_date',
                    'event_start_time',
                    'event_end_time',
                    'categories',
                    'is_online',
                    'registration_link']
