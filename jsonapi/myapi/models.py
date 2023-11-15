from django.db import models

# Create your models here.
class Transcripts(models.Model):
    # Define your fields here
    name = models.CharField(max_length=255)
    # Add other fields as needed
    content = models.TextField(max_length=4000, default='Hello there')    
