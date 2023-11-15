from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Transcripts

# Your existing function
def spolocna_praca_funguje(request):
    return JsonResponse({
        "message": "Diky kamo za pomoc vcera, toto teraz bezi na Django development servery :)",
        "option": "Y"
    })

# Function to add a new Transcript
def add_transcript(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content', 'Hello there')  # 'Hello there' is the default content
        if name:  # Make sure name is provided
            Transcripts.objects.create(name=name, content=content)
            return HttpResponse('Transcript added successfully!')
    return render(request, 'add_transcript.html')  # Render a template with a form to add a transcript


# View to retrieve and display all Transcripts
def view_transcripts(request):
    transcripts = Transcripts.objects.all()
    return render(request, 'view_transcripts.html', {'transcripts': transcripts})

# View to delete a Transcript
def delete_transcript(request, id):
    transcript = get_object_or_404(Transcripts, id=id)
    transcript.delete()
    return redirect('view_transcripts')  # Redirect to the view that displays all transcripts