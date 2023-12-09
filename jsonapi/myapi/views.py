from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import Transcripts, UploadedFile, Video
from .forms import MediaUploadForm
from moviepy.editor import VideoFileClip
import whisper
import os
import threading
from uuid import uuid4



MEDIA_ROOT = settings.MEDIA_ROOT

# Your existing function
def message(request):
    return JsonResponse({
        "message": "Diky kamo za pomoc vcera, toto teraz bezi na Django development servery :)",
        "option": "Y"
    })

# Function to add a new Transcript
def add_transcript(request):
    message = ''  # Initialize an empty message
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content', 'Hello there')
        if name:  # Make sure name is provided
            Transcripts.objects.create(name=name, content=content)
            message = 'Transcript added successfully!'  # Set the success message
    return render(request, 'add_transcript.html', {'message': message})


# View to retrieve and display all Transcripts
def view_transcripts(request):
    transcripts = Transcripts.objects.all()
    return render(request, 'view_transcripts.html', {'transcripts': transcripts})

# View to delete a Transcript
@require_POST  # This decorator makes the view only accept POST requests
def delete_transcript(request, id):
    transcript = get_object_or_404(Transcripts, id=id)
    transcript.delete()
    return redirect('view_transcripts')  # Redirect to the view that displays all transcripts

def upload_media(request):
    message = ''
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)  # Save the uploaded file without committing to the DB
            
            # Access the uploaded file object
            file_obj = request.FILES.get('file')
            
            # Create a new filename with a UUID to avoid naming conflicts
            ext = os.path.splitext(file_obj.name)[1]
            unique_filename = f"{uuid4()}{ext}"
            file_obj.name = unique_filename
            
            if file_obj and file_obj.content_type.startswith('video'):
                uploaded_file.save()  # Now you can save it to the DB since it's a video
                video = Video(file=uploaded_file.file)
                video.save()
                thread = threading.Thread(target=process_video, args=(video.id,))
                thread.start()
                message = 'Upload successful. Processing video...'
            else:
                message = 'Upload successful. File is not a video.'
        else:
            message = 'Upload failed. Please try again.'
    else:
        form = MediaUploadForm()
    return render(request, 'upload_media.html', {'form': form, 'message': message})


def process_video(video_id):
    try:
        video = Video.objects.get(id=video_id)
        video_clip = VideoFileClip(video.file.path)

        base_filename = os.path.splitext(os.path.basename(video.file.name))[0]
        audio_file_name = f"{base_filename}.wav"
        
        # Use os.path.join to create the full path in the 'media' directory
        audio_file_location = os.path.join(MEDIA_ROOT, 'audio', audio_file_name)
        
        # Ensure the 'audio' directory exists
        os.makedirs(os.path.join(MEDIA_ROOT, 'audio'), exist_ok=True)

        video_clip.audio.write_audiofile(audio_file_location)    
        
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_location)
        
        video.transcript = result["text"]
        video.processed = True
        video.save()

        os.remove(audio_file_location)  # Clean up the audio file
    except Video.DoesNotExist:
        print(f"Video with id {video_id} does not exist.")