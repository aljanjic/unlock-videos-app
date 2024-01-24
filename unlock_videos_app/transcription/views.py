from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.http import JsonResponse
from django.conf import settings
from .models import Transcripts, UploadedFile
from .forms import MediaUploadForm
from moviepy.editor import VideoFileClip
import whisper
from openai import OpenAI
import os
import threading
from rest_framework.generics import ListAPIView
from .serializers import TranscriptsSerializer, UploadedFileSerializer



class TranscriptsList(ListAPIView):
    queryset = Transcripts.objects.all()
    serializer_class = TranscriptsSerializer

class UploadedFileList(ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

# Function to add a new Transcript
@require_http_methods(["GET", "POST"])
def add_transcript(request):
    message = ''  # Initialize an empty message
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content', 'Hello there')
        if name:  # Make sure name is provided
            Transcripts.objects.create(file_name=name, content=content)
            message = 'Transcript added successfully!'  # Set the success message
    return render(request, 'add_transcript.html', {'message': message})


# View to retrieve and display all Transcripts
@require_GET
def view_transcripts(request):
    transcripts = Transcripts.objects.order_by('-id')
    return render(request, 'view_transcripts.html', {'transcripts': transcripts})

# View to delete a Transcript
@require_POST  # This decorator makes the view only accept POST requests
def delete_transcript(request, id):
    transcript = get_object_or_404(Transcripts, id=id)
    transcript.delete()
    return redirect('view_transcripts')  # Redirect to the view that displays all transcripts

@require_http_methods(["GET", "POST"])
def upload_media(request):
    message = ''
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)  # Save the uploaded file without committing to the DB
            
            # Access the uploaded file object
            file_obj = request.FILES.get('file')
            
            # Check the file type and process accordingly
            if file_obj.content_type.startswith('video'):
                video = UploadedFile(file=uploaded_file.file)
                video.save()
                # Process video in a separate thread
                thread = threading.Thread(target=process_video, args=(video.id,))
                thread.start()
                message = 'Upload successful. Processing video...'
            elif file_obj.content_type.startswith('audio'):
                uploaded_file.save()  # Save the audio file to the DB
                # Process audio in a separate thread
                thread = threading.Thread(target=process_audio, args=(uploaded_file.id,))
                thread.start()
                message = 'Upload successful. Processing audio...'
            else:
                message = 'Upload successful but it will not be processed... File is not a video or audio'
        else:
            message = 'Upload failed. Please try again.'
    else:
        form = MediaUploadForm()
    return render(request, 'upload_media.html', {'form': form, 'message': message})

def process_audio(audio_file_id):
    try:
        audio_file = UploadedFile.objects.get(id=audio_file_id)
        audio_file_location = audio_file.file.path
        
        # Transcribe the audio file
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_location)
        
        # Create a transcript object
        transcript = Transcripts(file_name=audio_file.file.name, content=result["text"])
        transcript.processed = True
        transcript.save()

        # Optionally, delete the audio file after processing
        # os.remove(audio_file_location)
        print(f"Audio file transcript created.")
    except UploadedFile.DoesNotExist:
        print(f"Audio file with id {audio_file_id} does not exist.")


def process_video(video_id):
    try:
        video = UploadedFile.objects.get(id=video_id)
        video_clip = VideoFileClip(video.file.path)

        base_filename = os.path.splitext(os.path.basename(video.file.name))[0]
        audio_file_name = f"{base_filename}.wav"
        
        # Use os.path.join to create the full path in the 'media' directory
        audio_file_location = os.path.join(settings.MEDIA_ROOT, 'audio', audio_file_name)
        
        # Ensure the 'audio' directory exists
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'audio'), exist_ok=True)

        video_clip.audio.write_audiofile(audio_file_location)    
        
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_location)

        transcript = Transcripts(file_name=video.file.name, content=result["text"])
        transcript.processed = True
        transcript.save()

        # Save again the output to myapi_video table
        # video.transcript = result["text"]
        # video.processed = True
        # video.save()

        # os.remove(audio_file_location)  # Clean up the audio file
        print(f"Video transcript created.")
    except UploadedFile.DoesNotExist:
        print(f"Video with id {video_id} does not exist.")

@require_POST
def send_to_chatgpt(request, transcript_id):
    try:
        client = OpenAI()
        transcript = Transcripts.objects.get(id=transcript_id)
        content = transcript.content

        client.api_key = settings.OPENAI_API_KEY  # Set the API key

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[      
                {
                    "role": "system",
                    "content": "You are a helpful assistant that is summarizing provided transcripts."
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        
        response_content = chat_completion.choices[0].message.content  # Modify this line as per your response structure

        transcript.chatgpt_summary = response_content
        transcript.save()

        print('Response from chatGPT:', response_content) # Can delete later  

        transcripts = Transcripts.objects.all()
        return redirect('view_transcripts')

    except Transcripts.DoesNotExist:
        return JsonResponse({"error": "Transcript not found"}, status=404)
    

