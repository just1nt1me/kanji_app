from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Kanji, JLPTLevel
from .forms import KanjiTestForm
from .util import wordnet_similarity
from django.http import JsonResponse
import random

# return what we want user to see from "home" page
def home(request):
    return render(request, 'level-test/home.html')

def about(request):
    return render(request, 'level-test/about.html', {'title': 'About'})

def start_test(request):
    # Load a random deck of 50 kanji (10 from each level) and store them in the session.
    levels = ["n5", "n4", "n3", "n2", "n1"]
    kanji_deck = []
    for level in levels:
        kanji_for_level = list(Kanji.objects.filter(tags__level='n5').values_list('id', flat=True))
        kanji_deck.extend(random.sample(kanji_for_level, 10))

    request.session['kanji_deck'] = kanji_deck
    request.session['current_index'] = 0
    request.session['score'] = 0

    return redirect('kanji_test')


def kanji_test(request):
    current_index = request.session.get('current_index')
    kanji_deck = request.session.get('kanji_deck')

    if current_index >= len(kanji_deck):
        # All questions have been answered
        return render(request, 'test_complete.html', {'score': request.session.get('score')})

    current_kanji = Kanji.objects.get(id=kanji_deck[current_index])

    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        similarity = wordnet_similarity(user_answer, current_kanji.meaning)

        if similarity >= 0.7:
            request.session['score'] += 1
            is_correct = True
        else:
            is_correct = False

        request.session['current_index'] += 1

        # Return result as JSON for AJAX approach, or redirect for traditional approach.
        return JsonResponse({
            'is_correct': is_correct,
            'correct_answer': current_kanji.meaning
        })

    return render(request, 'kanji-test.html', {'kanji': current_kanji.expression})
