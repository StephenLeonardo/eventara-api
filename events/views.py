from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Event
from .serializers import EventSerializer, EventPostSerializer

# Create your views here.
class EventAPIView(APIView):
    
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = EventPostSerializer(data=request.data)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class EventDetails(APIView):
    def get_object(self, event_id):
        try:
            return Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    def get(self, request, event_id):
        event = self.get_object(event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
        
        
    def put(self, request, event_id):
        event = self.get_object(event_id)
        serializer = EventPostSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, event_id):
        event = self.get_object(event_id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)