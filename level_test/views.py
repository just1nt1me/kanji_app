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

    request.session.modified = True

    return redirect('kanji_test')

def kanji_test(request):
    # Ensure the types of session variables are as expected.
    current_index = int(request.session.get('current_index'))
    kanji_deck = request.session.get('kanji_deck', [])
    current_level_index = int(request.session.get('current_level_index'))
    levels = ["n5", "n4", "n3", "n2", "n1"]
    request.session['level_complete'] = False
    request.session.modified = True

    if request.session.get('current_index', 0) == 0:
        request.session['level_complete'] = False
        request.session.modified = True

    # Fetch current kanji
    current_kanji = Kanji.objects.get(id=kanji_deck[current_index])

    if request.method == 'POST':
        print("POST request received.")
        print(request.session['level_complete'])
        print(current_index)
        # Check if all kanjis in the current deck have been processed
        if request.session['level_complete'] == True:
            if int(request.session['score']) < 5:  # If score is less than 5
                return render(request, 'level-test/test-failed.html', {'score': request.session.get('score')})

            # Check if there are more levels left
            if current_level_index < len(levels) - 1:
                request.session['current_level_index'] += 1
                kanji_for_level = list(Kanji.objects.filter(tags__level=levels[current_level_index]).values_list('id', flat=True))
                request.session['kanji_deck'] = random.sample(kanji_for_level, 10)
                request.session['current_index'] = 0
                request.session['score'] = 0
                request.session.modified = True
                return redirect('kanji_test')
            else:
                # All questions have been answered and all levels cleared
                return render(request, 'level-test/test-complete.html', {'score': request.session.get('score')})

        user_answer = request.POST.get('answer')
        similarity = spacy_similarity(user_answer, current_kanji.meaning)
        prev_kanji = current_kanji.expression
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

        if current_index == 9:
            request.session['level_complete'] = True
            request.session.save()
        else:
            # Increment the current index
            request.session['current_index'] += 1
            print("New current index:", request.session['current_index'])
            current_index = request.session['current_index']
            current_kanji = Kanji.objects.get(id=kanji_deck[current_index])

        # Check if the request is AJAX
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'is_correct': is_correct,
                'prev_kanji': prev_kanji,
                'correct_answer': correct_answer,
                'score': request.session['score'],
                'index': request.session['current_index'],
                'kanji': current_kanji.expression,
                'level': levels[current_level_index]
            })

    request.session.modified = True
    return render(request, 'level-test/kanji-test.html', {'kanji': current_kanji.expression, 'level': levels[current_level_index]})


def test_complete(request):
    return render(request, 'level-test/test-complete.html', {'title': 'Test Complete'})

def test_failed(request):
    return render(request, 'level-test/test-failed.html', {'title': 'Test Failed'})
