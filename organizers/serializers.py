from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organization
            fields = ['organizer_id', 'name', 'abbreviation', 'photo', 'description']
            
            
class OrganizationPostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organization
            fields = ['name', 'photo', 'abbreviation', 'description']