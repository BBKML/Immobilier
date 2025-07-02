from django.urls import path
from django.shortcuts import render
from django.contrib import admin
from django.db.models import Count
from datetime import datetime, timedelta
from .models import Vehicule, Moto, Client, Proprietaire

def home_view(request):
    """Page d'accueil simple avec redirection vers l'admin"""
    return render(request, 'vehicules/home.html')

urlpatterns = [
    path('', home_view, name='home'),
] 