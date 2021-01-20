from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ['id', 'name']
            
            
class CategoryPostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ['name']
        
        # def update(self, instance, validated_data):
        #     fields=instance._meta.fields
        #     exclude=[]
        #     for field in fields:
        #         field=field.name.split('.')[-1] #to get coulmn name
        #         if field in exclude:
        #            continue
        #         exec("instance.%s = validated_data.get(field, instance.%s)"%(field,field))
        #     instance.save()
        #     return instance