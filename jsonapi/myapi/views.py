from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Transcripts, UploadedFile, Video
from .forms import MediaUploadForm
from moviepy.editor import VideoFileClip
import whisper
import os
import threading


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
    video_id = None  # Initialize video_id as None
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Save the file and get the instance back
            # Check if uploaded file is a video by its MIME type or file extension
            if 'video' in uploaded_file.file.content_type:
                # Assign the ID of the saved video to video_id
                video_id = uploaded_file.id
                # Process video in a separate thread to avoid blocking
                thread = threading.Thread(target=process_video, args=(uploaded_file.id,))
                thread.start()
                message = 'Upload successful. Processing video...'
            else:
                message = 'Upload successful'
        else:
            message = 'Upload failed. Please try again.'
    else:
        form = MediaUploadForm()
    # Pass video_id to the template
    return render(request, 'upload_media.html', {'form': form, 'message': message, 'video_id': video_id})


def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video_clip = VideoFileClip(video.file.path)
    audio_file_location = '/path/to/audio/output.wav'
    video_clip.audio.write_audiofile(audio_file_location)
    
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_location)
    
    video.transcript = result["text"]
    video.processed = True
    video.save()

    os.remove(audio_file_location)  # Clean up the audio file