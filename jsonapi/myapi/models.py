from django.db import models

# Create your models here.
class Transcripts(models.Model):
    # Define your fields here
    name = models.CharField(max_length=255)
    # Add other fields as needed
    content = models.TextField(max_length=4000, default='Hello there')    

class TranscriptDetail(models.Model):
    name = models.CharField(max_length=255)
    length = models.PositiveIntegerField(help_text="Length of the transcript in characters")

    def __str__(self):
        return f"{self.name} - {self.length} characters"
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='files/') # 'files/' is the directory where files will be stored'
    uploaded_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded on {self.uploaded_at}"
    
class Video(models.Model):
    file = models.FileField(upload_to='videos/')
    transcript = models.TextField(blank=True)
    processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    