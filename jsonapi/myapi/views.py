from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def dummy_data(request):
    return JsonResponse({"message": "Hello, this is dummy data"})
