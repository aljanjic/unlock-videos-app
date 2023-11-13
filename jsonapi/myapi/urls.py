from django.urls import path
from . import views

urlpatterns = [
    path('api/dummydata', views.dummy_data, name='dummy_data'),
]