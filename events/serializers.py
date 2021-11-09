from django.db.models import fields
from rest_framework import serializers
from .models import Event, EventImage

from categories.serializers import CategorySerializer
from organizers.serializers import OrganizerSerializer
from accounts.serializers import AccountSerializer


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        exclude = ['event']



class EventSerializer(serializers.ModelSerializer):
    organizer = AccountSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    event_images = EventImageSerializer(many=True, read_only=True)
    thumbnail = serializers.SerializerMethodField()

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
                    'registration_link',
                    'event_images',
                    'thumbnail']

    
    def get_thumbnail(self, instance):
        thumbnail = instance.event_images.all()
        return EventImageSerializer(thumbnail[0]).data

class EventListSerializer(serializers.ModelSerializer):
    organizer = AccountSerializer()
    # thumbnail = EventImageSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['event_id',
                    'name',
                    'image',
                    'organizer',
                    'event_date',
                    'thumbnail']


    def get_thumbnail(self, instance):
        thumbnail = instance.event_images.all().order_by('image_order')
        if thumbnail:
            return EventImageSerializer(thumbnail[0]).data
        return None


class EventPostSerializer(serializers.ModelSerializer):
    # organizer_username = serializers.CharField()

    def to_internal_value(self, data):
        if 'categories' in data and data['categories'] == '':
            _mutable = data._mutable
            data._mutable = True
            data.pop('categories')
            data._mutable = _mutable
        return super(EventPostSerializer,self).to_internal_value(data)
    class Meta:
        model = Event
        fields = ['name',
                    'description',
                    # 'organizer_username',
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
