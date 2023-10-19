from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Kanji, JLPTLevel
from .forms import KanjiTestForm
from .util import spacy_similarity
from django.http import JsonResponse
import random

# return what we want user to see from "home" page
def home(request):
    return render(request, 'level-test/home.html')

def about(request):
    return render(request, 'level-test/about.html', {'title': 'About'})

def start_test(request):
    # Start with only the first level
    levels = ["n5", "n4", "n3", "n2", "n1"]
    kanji_deck = []
    kanji_for_level = list(Kanji.objects.filter(tags__level=levels[0]).values_list('id', flat=True))
    kanji_deck.extend(random.sample(kanji_for_level, 10))

    request.session['kanji_deck'] = kanji_deck
    request.session['current_index'] = 0
    request.session['score'] = 0
    request.session['current_level_index'] = 0

    return redirect('kanji_test')

def kanji_test(request):
    # Ensure the types of session variables are as expected.
    current_index = int(request.session.get('current_index', 0))
    kanji_deck = request.session.get('kanji_deck', [])
    current_level_index = int(request.session.get('current_level_index', 0))
    levels = ["n5", "n4", "n3", "n2", "n1"]

    if current_index >= 10:  # If 10 questions have been answered
        if int(request.session['score']) < 5:  # If score is less than 5
            return render(request, 'test_failed.html', {'score': request.session.get('score')})

        # Check if there are more levels left
        if current_level_index < len(levels) - 1:
            current_level_index += 1
            request.session['current_level_index'] = current_level_index
            kanji_for_level = list(Kanji.objects.filter(tags__level=levels[current_level_index]).values_list('id', flat=True))
            request.session['kanji_deck'] = random.sample(kanji_for_level, 10)
            request.session['current_index'] = 0
            current_index = 0
            kanji_deck = request.session.get('kanji_deck')
        else:
            # All questions have been answered and all levels cleared
            return render(request, 'test_complete.html', {'score': request.session.get('score')})

    current_kanji = Kanji.objects.get(id=kanji_deck[current_index])

    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        similarity = spacy_similarity(user_answer, current_kanji.meaning)
        correct_answer = current_kanji.meaning

        if similarity >= 0.8:
            request.session['score'] += 1
            is_correct = True
        else:
            is_correct = False

        # Print feedback and score to the terminal
        if is_correct:
            print(f"Correct! Answer: {user_answer}, Expected: {current_kanji.meaning}")
        else:
            print(f"Incorrect. Answer: {user_answer}, Expected: {current_kanji.meaning}")
        print(f"Current Score: {request.session['score']}")

        request.session['current_index'] += 1
        current_kanji = Kanji.objects.get(id=kanji_deck[int(request.session['current_index'])])  # Fetch the next kanji

        # Check if the request is AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return result as JSON for AJAX
            return JsonResponse({
                'is_correct': is_correct,
                'correct_answer': correct_answer,
                'score': request.session['score'],
                'kanji': current_kanji.expression  # Add the next kanji to the JSON response
            })

    # For GET requests and non-AJAX POST requests
    return render(request, 'level-test/kanji-test.html', {'kanji': current_kanji.expression, 'level': levels[current_level_index]})
