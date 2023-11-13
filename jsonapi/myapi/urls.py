from django.urls import path
from . import views

urlpatterns = [
    path('api/dummydata', views.spolocna_praca_funguje, name='dummy_data'),
]