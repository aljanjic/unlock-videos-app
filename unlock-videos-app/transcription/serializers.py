from rest_framework import serializers
from .models import Transcripts, UploadedFile

class TranscriptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcripts
        fields = ['id', 'file_name', 'processed_time', 'processed', 'content', 'chatgpt_summary']

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'upload_time']
