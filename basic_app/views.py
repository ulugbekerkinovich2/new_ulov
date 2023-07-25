import os.path
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from rest_framework import generics, filters
from . import models
from . import serializers
from rest_framework.response import Response


class PageNumberPagination(PageNumberPagination):
    page_size = 2


# Create your views here.
class ListFile(generics.ListCreateAPIView):
    queryset = models.Upload_File.objects.all().order_by('-id')
    serializer_class = serializers.UploadFileSerializer
    pagination_class = PageNumberPagination


class ListFile2(generics.ListCreateAPIView):
    queryset = models.Upload_File2.objects.all().order_by('-id')
    serializer_class = serializers.UploadFile2Serializer
    pagination_class = PageNumberPagination


# class ListData21(generics.ListCreateAPIView):
#     queryset = models.Data21.objects.all()
#     serializer_class = serializers.Data21Serializer
#     pagination_class = PageNumberPagination
