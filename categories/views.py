from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer, CategoryPostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.settings import api_settings
from django.shortcuts import get_object_or_404


class CategoryView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = CategoryPostSerializer
    queryset = Category.objects.all()
    
    
    
    
    def list(self, request):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        
        list_categories = Category.objects.all()
        categories = paginator.paginate_queryset(list_categories, request)
        
        serializer = CategorySerializer(categories, many=True)
        return Response({
            'Status': True,
            'Message': 'Wow it worked!',
            'Data': paginator.get_paginated_response(serializer.data).data
        })
    
    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response({
            'Status': True,
            'Message': 'Wow it worked!',
            'Data': serializer.data
        })
    
    def create(self, request):
        serializer = CategoryPostSerializer(data=request.data)
        
        if serializer.is_valid():
            category = Category.objects.create(**serializer.data)
            category.save()
            
            result_serializer = CategorySerializer(category)
            
            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': result_serializer.data,
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            queryset = Category.objects.all()
            category = get_object_or_404(queryset, pk=pk)
            category.delete()
            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': None,
            })
        except:
            raise
    
    def update(self, request, pk=None):
        serializer = CategoryPostSerializer(data=request.data)
        if serializer.is_valid():
            queryset = Category.objects.all()
            category = get_object_or_404(queryset, pk=pk)
            
            category.name = serializer.data.get('name', '')
            category.save()
            
            result_serializer = CategorySerializer(category)
            return Response({
                'Status': True,
                'Message': 'Wow it worked!',
                'Data': result_serializer.data,
            })
        


# Create your views here.
# class CategoryAPIView(APIView):
# 
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
# 
#     def post(self, request):
#         serializer = CategoryPostSerializer(data=request.data)
# 
# 
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
# 
# class CategoryDetails(APIView):
#     def get_object(self, id):
#         try:
#             return Category.objects.get(id=id)
#         except Category.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
# 
#     def get(self, request, id):
#         category = self.get_object(id)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
# 
# 
#     def put(self, request, id):
#         category = self.get_object(id)
#         serializer = CategoryPostSerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
#     def delete(self, request, id):
#         category = self.get_object(id)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)