"""
URL configuration for unlock_videos_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import RedirectView
from transcription import views
from transcription.views import TranscriptsList, UploadedFileList, add_transcript_form, add_transcript_submit

urlpatterns = [
    path('', RedirectView.as_view(url='/view/'), name='go-to-view'),
    path('admin/', admin.site.urls),
    path('transcription/', include('transcription.urls')),
    path('add/', add_transcript_form, name='add_transcript_form'),
    path('add/submit/', add_transcript_submit, name='add_transcript_submit'),
    path('view/', views.view_transcripts, name='view_transcripts'),
    path('upload-media/', views.upload_media_form, name='upload_media_form'),
    path('upload-media/submit/', views.upload_media_submit, name='upload_media_submit'),
    path('delete/<int:id>/', views.delete_transcript, name='delete_transcript'),
    path('send_to_chatgpt/<int:transcript_id>/', views.update_transcript_with_chatgpt, name='update_transcript_with_chatgpt'),
    path('api/transcripts/', TranscriptsList.as_view(), name='transcripts-list'),
    path('api/uploadedfiles/', UploadedFileList.as_view(), name='uploadedfiles-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
