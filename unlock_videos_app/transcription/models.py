from django.db import models

# Create your models here.
class Transcripts(models.Model):
    # Define your fields here
    file_name = models.CharField(max_length=255)
    # Add other fields as needed
    processed_time= models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    content = models.TextField(max_length=4000)
    chatgpt_summary = models.TextField(blank=True, default='')  # Field to store ChatGPT summarization
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='files/') # 'files/' is the directory where files will be stored'
    upload_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File uploaded on {self.upload_time}"

    