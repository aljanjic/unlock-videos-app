from django.urls import path
from . import views

urlpatterns = [
    path('message', views.message, name='message'),
    path('add/', views.add_transcript, name='add_transcript'),
    path('view/', views.view_transcripts, name='view_transcripts'),
    path('delete/<int:id>/', views.delete_transcript, name='delete_transcript'),
    path('upload-media', views.upload_media, name='upload_media'),
    path('send_to_chatgpt/<int:transcript_id>/', views.send_to_chatgpt, name='send_to_chatgpt')
]