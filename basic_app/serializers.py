from rest_framework import serializers
from . import models


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Upload_File
        fields = '__all__'


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mark
        fields = '__all__'


class UploadFile2Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Upload_File2
        fields = '__all__'
