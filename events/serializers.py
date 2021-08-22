from django.db import models
from rest_framework import serializers
from .models import Event, EventImage

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
                    'images',
                    'organizer',
                    'location',
                    'event_date',
                    'event_start_time',
                    'event_end_time',
                    'categories',
                    'is_online',
                    'registration_link']

class EventListSerializer(serializers.ModelSerializer):
    organizer = AccountSerializer()

    class Meta:
        model = Event
        # fields = '__all__'
        fields = ['event_id',
                    'name',
                    'images',
                    'organizer',
                    'event_date']


class EventPostSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField()
    images = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Event
        fields = ['name',
                    'description',
                    'images',
                    'organizer_username',
                    'location',
                    'event_date',
                    'event_start_time',
                    'event_end_time',
                    'categories',
                    'is_online',
                    'registration_link']


class EventByCategorySerializer(serializers.Serializer):
    category_list = serializers.ListField(
                       child=serializers.IntegerField()
                    )
