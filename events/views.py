from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import (LimitOffsetPagination,
                                        PageNumberPagination)
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .models import Event
from .serializers import EventSerializer, EventPostSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.settings import api_settings



class EventGenericViewSet(viewsets.GenericViewSet):
                            
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return EventSerializer
        if self.action == 'create':
            return EventPostSerializer
    
    
    def list(self, request):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        
        list_events = Event.objects.all()
        events = paginator.paginate_queryset(list_events, request)
        
        serializer = EventSerializer(events, many=True)
        return Response({
            'Status': 'Success',
            'Message': 'Wow it worked!',
            'Data': paginator.get_paginated_response(serializer.data).data
        })
    
    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)
        serializer = EventSerializer(instance=event)
        return Response({
            'Status': 'Success',
            'Message': 'Wow it worked!',
            'Data': serializer.data
        })
    
    def create(self, request):
        serializer = EventPostSerializer(data=request.data)
        
        if serializer.is_valid():
            event = Event.objects.create(**serializer.data)
            event.save()
            
            result_serializer = EventSerializer(instance=event)
            
            return Response({
                'Status': 'Success',
                'Message': 'Wow it worked!',
                'Data': result_serializer.data,
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class EventGenericPostViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
#                             mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
#                             mixins.DestroyModelMixin):
#     permission_classes = [IsAuthenticated]
#     serializer_class = EventPostSerializer
#     queryset = Event.objects.all()       
    
    



# class EventViewset(viewsets.ViewSet):
#     def list(self, request):
#         events = Event.objects.all()
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)
# 
#     def create(self, request):
#         serializer = EventPostSerializer(data=request.data)
# 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
#     def retrieve(self, request, pk=None):
#         queryset = Event.objects.all()
#         event = get_object_or_404(queryset, pk=pk)
#         serializer = EventSerializer(event)
#         return Response(serializer.data)
# 
#     def update(self, request, pk=None):
#         event = Event.objects.get(pk=pk)
#         serializer = EventPostSerializer(event, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
# 
# 
# class EventGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin):
#     serializer_class = EventSerializer
#     queryset = Event.objects.all()
# 
#     def get(self, request):
#         return self.list(request=request)
# 
# 
# 
# # Create your views here.
# class EventAPIView(APIView, LimitOffsetPagination):
#     permission_classes = [AllowAny]    
#     def get(self, request):
#         self.default_limit = 20
#         events = Event.objects.all()
#         results = self.paginate_queryset(events, request, view=self)
#         serializer = EventSerializer(results, many=True)
#         return self.get_paginated_response(serializer.data)
# 
# 
# class EventPostView(APIView):
#     permission_classes = [IsAuthenticated,]
#     def post(self, request):
#         serializer = EventPostSerializer(data=request.data)
# 
# 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
# class EventDetailsPutDeleteView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get_object(self, event_id):
#         try:
#             return Event.objects.get(event_id=event_id)
#         except Event.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
# 
# 
#     def put(self, request, event_id):
#         event = self.get_object(event_id)
#         serializer = EventPostSerializer(event, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
#     def delete(self, request, event_id):
#         event = self.get_object(event_id)
#         event.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# 
# class EventDetails(APIView):
# 
#     permission_classes = [AllowAny]
#     def get_object(self, event_id):
#         try:
#             return Event.objects.get(event_id=event_id)
#         except Event.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
# 
#     def get(self, request, event_id):
#         event = self.get_object(event_id)
#         serializer = EventSerializer(event)
#         return Response(serializer.data)
    
    