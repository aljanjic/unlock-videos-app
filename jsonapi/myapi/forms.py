from django import forms
from .models import UploadedFile
from django.core.exceptions import ValidationError
import os

class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1]
        valid_extensions = ['.mp4', '.mov', '.avi', '.jpg', '.jpeg', '.png']
        if not extension.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')
        return file