from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from .models import Transcripts, UploadedImage
from .forms import ImageUploadForm



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
    message=''
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message='Upload successful'
            form = ImageUploadForm()
        else:
            message = 'Upload failed. Please try again.'
    else:
        form = ImageUploadForm()
    return render(request, 'upload_media.html', {'form': form, 'message': message})