import time
import json
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

from .utils import path_and_rename
from .models import Event, EventImage
from .serializers import (EventSerializer, EventPostSerializer,
                            EventListSerializer)
from rest_framework import viewsets
from rest_framework.settings import api_settings
from django.conf import settings

from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()


class EventGenericViewSet(mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()



    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == 'retrieve':
            return EventSerializer
        elif (self.action == 'create' or self.action == 'update'
            or self.action == 'partial_update'):
            return EventPostSerializer
        elif self.action == 'get_by_categories':
            return EventSerializer

    def list(self, request):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()

        queryset = None

        category_list = request.query_params.get('category_id', [])
        if  len(category_list) > 0:
            category_list = list(map(int, category_list.split(',')))
            queryset = Event.objects.filter(
                                        categories__in=category_list).order_by('-created_date').prefetch_related('organizer')
        else:
            queryset = Event.objects.all().order_by('-created_date').prefetch_related('organizer')
        


        events = paginator.paginate_queryset(queryset, request)

        serializer = EventListSerializer(events, many=True)

        return Response({
            'Status': True,
            'Message': 'Wow it worked!',
            'Data': paginator.get_paginated_response(serializer.data).data
        })

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)
        serializer = EventSerializer(instance=event)
        return Response({
            'Status': True,
            'Message': 'Wow it worked!',
            'Data': serializer.data
        })

    def create(self, request):
        serializer = EventPostSerializer(data=request.data)

        if serializer.is_valid():
            serialized_data = serializer.data
            images = serialized_data.pop('images', [])
            category_list = serialized_data.pop('categories', [])

            event = Event.objects.create(**serialized_data, organizer=request.user)
            event.categories.set(category_list)
            event.save()

            for index, item in enumerate(images):
                y = json.loads(item)
                EventImage.objects.create(**y, event=event, image_order=index+1).save()

            result_serializer = EventSerializer(instance=event)

            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': result_serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        serializer = EventPostSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        instance = self.get_object()

        category_list = serialized_data.pop('categories', [])  
        
        images = serialized_data.pop('images', [])
        serialized_data['images'] = []
        
        instance.categories.set(category_list)


        update_serializer = EventPostSerializer(instance, data=serialized_data, partial=False)
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()

        # Delete all event images and add them again
        EventImage.objects.filter(event=instance).delete()

        for index, item in enumerate(images):
            y = json.loads(item)
            EventImage.objects.create(**y, event=instance, image_order=index+1).save()


        result_serializer = EventSerializer(instance=instance)

        return Response({
            'Status': True,
            'Message': 'Wow it worked!',
            'Data': result_serializer.data,
        }, status=status.HTTP_200_OK)


    
    @action(methods=['post'], permission_classes=[IsAuthenticated], detail=False)
    def image(self, request):
        if 'image' in request.FILES:
            image = request.FILES['image']

            valid_extensions = ['jpeg', '.jpg', '.png', 'jfif', 'webp']
            ext = image.name.split('.')[-1]

            if not ext.lower() in valid_extensions:
                return Response({
                        'Status': False,
                        'Message': 'image must be in jpeg, jpg, png, jfif, or webp format',
                    }, status=status.HTTP_400_BAD_REQUEST)

            i = Image.open(image)
            thumb_io = BytesIO()
            month_year = time.strftime("%m-%Y")
            
            i.save(thumb_io, format='webp', quality=75, save_all=True)
            compressed_image = ContentFile(thumb_io.getvalue())

            path = storage.save('events/{}/{}'.format(month_year, path_and_rename(request.user.id, image.name)), compressed_image)
            full_path = '{}{}'.format(settings.MEDIA_URL, path)


            return Response({
                    'Status': True,
                    'Message': 'Wow it worked!',
                    'Data': {'image_url': full_path},
                }, status=status.HTTP_201_CREATED)

        return Response({
                'Status': False,
                'Message': 'No image detected',
            }, status=status.HTTP_400_BAD_REQUEST)