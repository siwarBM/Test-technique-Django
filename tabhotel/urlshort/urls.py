from django.shortcuts import redirect
from django.urls import path
from .views import home, createShortURL, ShortRedirectView, redirect

urlpatterns = [
    path('', home, name='home'),
    path('create/', createShortURL, name='create'),
    path('<str:url>', redirect, name='redirect')
    
]