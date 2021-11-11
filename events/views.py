import time
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

import categories
from .models import Event, EventImage
from .serializers import (EventSerializer, EventPostSerializer,
                            EventByCategorySerializer, EventListSerializer, EventPostUrlSerializer)
from rest_framework import viewsets
from rest_framework.settings import api_settings
from django.conf import settings

from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()


class EventGenericViewSet(mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly, AllowAny] # For development purposes
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

            if 'image' in request.FILES:
                image = request.FILES['image']

                if image:
                    # month_year = time.strftime("%m-%Y")
                    # path = storage.save('events/{}/{}'.format(month_year, image.name), image)
                    # full_path = '{}{}'.format(settings.MEDIA_URL, path)
                    serialized_data['image'] = image
                                    
            category_list = serialized_data.pop('categories', [])

            event = Event.objects.create(**serialized_data, organizer=request.user)
            event.categories.set(category_list)

            event.save()

            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for index, image in enumerate(images):
                    month_year = time.strftime("%m-%Y")
                    path = storage.save('events/{}/{}'.format(month_year, image.name), image)
                    full_path = '{}{}'.format(settings.MEDIA_URL, path)

                    # if index == 0:
                    #     event.update(image=full_path)

                    event_image = EventImage.objects.create(image=full_path, event=event, image_order=index+1)
                    event_image.save()


            result_serializer = EventSerializer(instance=event)

            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': result_serializer.data,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):

        # serializer = EventPostSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer_data = serializer.data

        # event = self.get_object()

        # if 'image' in request.FILES:
        #     image = request.FILES['image']

        #     if image:
        #         month_year = time.strftime("%m-%Y")
        #         path = storage.save('events/{}/{}'.format(month_year, image.name), image)
        #         full_path = '{}{}'.format(settings.MEDIA_URL, path)
        #         serializer_data['image'] = full_path


        # category_list = serializer_data.pop('categories', [])
        # # event = Event.objects.create(**serializer_data, organizer=request.user)
        # event.categories.set(category_list)
        # event.save()


        # if 'images' in request.FILES:
        #     images = request.FILES.getlist('images')
        #     for index, image in enumerate(images):
        #         month_year = time.strftime("%m-%Y")
        #         path = storage.save('events/{}/{}'.format(month_year, image.name), image)
        #         full_path = '{}{}'.format(settings.MEDIA_URL, path)

        #         # if index == 0:
        #         #     event.update(image=full_path)

        #         event_image = EventImage.objects.create(image=full_path, event=event, image_order=index+1)
        #         event_image.save()

        # result_serializer = EventSerializer(instance=event)
        # return Response({
        #     'Status': True,
        #     'Message': 'Wow it worked!',
        #     'Data': result_serializer.data,
        # }, status=status.HTTP_202_ACCEPTED)
        

        
        


        serializer = EventPostSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        instance = self.get_object()

        if 'image' in request.FILES:
            image = request.FILES['image']

            if image:
                # month_year = time.strftime("%m-%Y")
                # path = storage.save('events/{}/{}'.format(month_year, image.name), image)
                # full_path = '{}{}'.format(settings.MEDIA_URL, path)
                # serialized_data['image'] = full_path
                serialized_data['image'] = image

        category_list = serialized_data.pop('categories', [])  
        
        instance.categories.set(category_list)


        update_serializer = EventPostSerializer(instance, data=serialized_data, partial=False)
        update_serializer.is_valid(raise_exception=True)
        update_serializer.save()

        # Delete all event images and add them again
        EventImage.objects.filter(event=instance).delete()
        if 'images' in request.FILES:
            images = request.FILES.getlist('images')
            for index, image in enumerate(images):
                # month_year = time.strftime("%m-%Y")
                # path = storage.save('events/{}/{}'.format(month_year, image.name), image)
                # full_path = '{}{}'.format(settings.MEDIA_URL, path)

                # if index == 0:
                #     event.update(image=full_path)

                event_image = EventImage.objects.create(image=image, event=instance, image_order=index+1)
                event_image.save()

        # instance.save()

        result_serializer = EventSerializer(instance=instance)

        return Response({
            'Status': True,
            'Message': 'Wow it worked!',
            'Data': result_serializer.data,
        }, status=status.HTTP_200_OK)


        
                

    
    # @swagger_auto_schema(method='POST')
    # @action(detail=False, methods=['POST'])
    # def create_with_image_url(self, request):
    #     serializer = EventPostUrlSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serialized_data = serializer.data
    #         serialized_data['organizer'] = Account.objects.get(
    #                                 username=serialized_data.pop('organizer_username', None)
    #                                 )
                                    
    #         category_list = serialized_data.pop('categories', [])

    #         event = Event.objects.create(**serialized_data)
    #         event.categories.set(category_list)
    #         event.save()

    #         result_serializer = EventSerializer(instance=event)

    #         return Response({
    #             'Status': True,
    #             'Message': 'Wow it worked!',
    #             'Data': result_serializer.data,
    #         })

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # category_id_param = openapi.Parameter('category_id', in_=openapi.IN_QUERY,
    #                      description='Category ID, you can specify more that one etc: ?category_id=2&category_id=3...',
    #                      type=openapi.TYPE_INTEGER, required=True)
    # @swagger_auto_schema(manual_parameters=[category_id_param], method='GET')
    # @action(detail=False, methods=['GET'])
    # def get_by_categories(self, request):

    #     # serializer = EventByCategorySerializer(data=request.query_params)
    #     category_list = request.query_params.get('category_id', [])
    #     if  len(category_list) > 0:
    #         category_list = list(map(int, category_list.split(',')))
    #     


    #     # request_serializer = CategoryPostSerializer(data=category_list,
    #     #                                             many=True)


    #     try:
    #         pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    #         paginator = pagination_class()

    #         list_events = Event.objects.filter(
    #                                     categories__in=category_list).order_by('-created_date')
    #         events = paginator.paginate_queryset(list_events, request)

    #         serializer = EventSerializer(events, many=True)
    #         return Response({
    #             'Status': True,
    #             'Message': 'Wow it worked!',
    #             'Data': paginator.get_paginated_response(serializer.data).data
    #         })
    #     except Exception as e:
    #         return Response({
    #             'Status': False,
    #             'Message': str(e),
    #         }, status=status.HTTP_400_BAD_REQUEST)
