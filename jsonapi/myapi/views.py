from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def spolocna_praca_funguje(request):
    return JsonResponse({
        "message": "Diky kamo za pomoc vcera, toto teraz bezi na Django development servery :)",
        "option": "Y"
        })
