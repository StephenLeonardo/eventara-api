from rest_framework import serializers
from rest_framework.fields import ListField
from .models import Event, EventImage

from categories.serializers import CategorySerializer
from accounts.serializers import AccountSerializer


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        exclude = ['event']

class EventImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        exclude = ['event', 'id']


class EventSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    # images = EventImageSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['event_id',
                    'name',
                    'description',
                    'image',
                    'author',
                    'location',
                    'event_date',
                    'event_start_time',
                    'event_end_time',
                    'categories',
                    'is_online',
                    'registration_link',
                    'images',
                    'thumbnail']

    def get_images(self, instance):
        images = instance.images.all().order_by('image_order')
        return EventImageSerializer(images, many=True).data
    
    def get_thumbnail(self, instance):
        thumbnail = instance.images.all().order_by('image_order')
        if thumbnail:
            return EventImageSerializer(thumbnail[0]).data
        return None

class EventListSerializer(serializers.ModelSerializer):
    author = AccountSerializer()
    # thumbnail = EventImageSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['event_id',
                    'name',
                    'image',
                    'author',
                    'event_date',
                    'thumbnail']


    def get_thumbnail(self, instance):
        thumbnail = instance.images.all().order_by('image_order')
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

    # images = EventImagePostSerializer(many=True)
    images = ListField(child=serializers.CharField())
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
                    'registration_link',
                    'image',
                    'images']


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