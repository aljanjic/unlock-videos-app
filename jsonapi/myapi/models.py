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