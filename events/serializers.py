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

class EventListSerializer(serializers.ModelSerializer):
    organizer = AccountSerializer()

    class Meta:
        model = Event
        fields = ['event_id',
                    'name',
                    'image',
                    'organizer',
                    'event_date']


class EventPostSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField()
    image_blob = serializers.FileField()
    class Meta:
        model = Event
        fields = ['name',
                    'description',
                    'image_blob',
                    'organizer_username',
                    'location',
                    'event_date',
                    'event_start_time',
                    'event_end_time',
                    'categories',
                    'is_online',
                    'registration_link']


class EventPostUrlSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField()
    class Meta:
        model = Event
        fields = ['name',
                    'description',
                    'image_url',
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
