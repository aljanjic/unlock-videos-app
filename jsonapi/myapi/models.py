from django.db import models

# Create your models here.
class Transcripts(models.Model):
    # Define your fields here
    name = models.CharField(max_length=255)
    # Add other fields as needed
    uploaded_at= models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    content = models.TextField(max_length=4000, default='Hello there')
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='files/') # 'files/' is the directory where files will be stored'
    uploaded_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded on {self.uploaded_at}"

    