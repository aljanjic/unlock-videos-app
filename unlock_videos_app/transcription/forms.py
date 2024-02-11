from django import forms
from .models import UploadedFile, Transcripts
from django.core.exceptions import ValidationError
import magic

class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class TranscriptForm(forms.ModelForm):
    class Meta:
        model = Transcripts
        fields = ['file_name', 'content']  # Adjust the fields based on your model


    def clean_file(self):
        file = self.cleaned_data['file']
        # Check file size
        if file.size > 50*1024*1024:  # 50MB limit
            raise ValidationError('File too large. Size should not exceed 50 MB.')

        # Check file content type
        mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)  # Reset file pointer after reading
        valid_mimes = [
            'audio/mpeg',   # For .mp3
            'audio/x-wav',  # For .wav
            'audio/x-aiff', # For .aiff
            'audio/flac',   # For .flac
            'video/mp4',    # For .mp4
            'video/x-msvideo', # For .avi
            'video/quicktime' # For .mov
            # Add other MIME types as needed
        ]
        if mime not in valid_mimes:
            raise ValidationError('Unsupported file type.')

        return file