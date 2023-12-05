from django.shortcuts import render, redirect
from .models import UserKanjiProgress

def study(request):
    return render(request, 'study-decks/study.html')

def deck(request):
    return render(request, 'study-decks/deck.html')
