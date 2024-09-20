from rest_framework import serializers
from core import models
from datetime import datetime
from . import serializers as client_serializer


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Client
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    date_uploaded = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        fields = [
            'memo_number',
            'client',
            'date_uploaded',
            'start',
            'end',
            'ftp',
            'title',
            'department',
            'description',
            'text',
            'status'
        ]

    ftp = serializers.SerializerMethodField(
        'fetch_ftp'
    )

    def get_date_uploaded(self, obj):
        return datetime.strftime(obj.date_uploaded, '%B %d, %Y')

    def get_start(self, obj):
        return datetime.strftime(obj.start, '%B %d, %Y')

    def get_end(self, obj):
        return datetime.strftime(obj.end, '%B %d, %Y')

    def fetch_ftp(self, obj):
        result = []
        df = models.NewsFile.objects.filter(
            news__id=obj.id
        )

        if df:
            result = client_serializer.NewsFilesSerializer(
                instance=df,
                many=True
            ).data

        return result


class DocumentFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DocumentFiles
        fields = '__all__'


class NewsFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NewsFile
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.SerializerMethodField()

    class Meta:
        model = models.Document
        fields = [
            'id',
            'control_number',
            'client',
            'department',
            'date',
            'title',
            'status',
            'uploaded_by',
            'description',
            'files',
            'date_uploaded'
        ]

    files = serializers.SerializerMethodField(
        'fetch_files'
    )

    def get_uploaded_by(self, obj):
        result = ''
        if obj.uploaded_by:
            result = '%s %s' % (
                obj.uploaded_by.first_name,
                obj.uploaded_by.last_name
            )
        return result.title()

    def fetch_files(self, obj):
        result = []
        df = models.DocumentFiles.objects.filter(
            document__id=obj.id
        )

        if df:
            result = client_serializer.DocumentFilesSerializer(
                instance=df,
                many=True
            ).data

        return result


class DepartmentSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = models.Department
        fields = [
            'id',
            'name',
            'info',
            'active',
            'representative',
            'value'
        ]

    def get_value(self, obj):
        return obj.id
