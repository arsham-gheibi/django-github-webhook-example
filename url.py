from django.urls import path
from . import views

path('deploy_webhook/',
     views.webhook,
     name='webhook'),
