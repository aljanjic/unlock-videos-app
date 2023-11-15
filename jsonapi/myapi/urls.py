from django.urls import path
from . import views

urlpatterns = [
    path('api/dummydata', views.spolocna_praca_funguje, name='dummy_data'),
    path('add/', views.add_transcript, name='add_transcript'),
    path('view/', views.view_transcripts, name='view_transcripts'),
    path('delete/<int:id>/', views.delete_transcript, name='delete_transcript'),
]