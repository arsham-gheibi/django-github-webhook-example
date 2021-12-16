from django.urls import path
from . import views

path('webhook/',
     views.webhook,
     name='webhook'),
