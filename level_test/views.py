from django.shortcuts import render, redirect
from .models import Kanji
from .utils import handle_test_completion_or_advancement, check_answer_similarity
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
    kanji_for_level = list(Kanji.objects.filter(jlpt_level=levels[0]).values_list('id', flat=True))
    kanji_deck.extend(random.sample(kanji_for_level, 10))

    request.session['kanji_deck'] = kanji_deck
    request.session['current_index'] = 0
    request.session['score'] = 0
    request.session['current_level_index'] = 0

    request.session['kanji'] = []
    request.session['correct'] = []
    request.session['correct_answers'] = []
    request.session['user_answers'] = []
    request.session['level_scores'] = {level: 0 for level in levels}

    request.session.modified = True

    return redirect('kanji_test')

def kanji_test(request):
    if request.method == 'GET':
        return kanji_test_get(request)
    elif request.method == 'POST':
        return kanji_test_post(request)

def kanji_test_get(request):
    current_index = int(request.session.get('current_index'))
    kanji_deck = request.session.get('kanji_deck', [])
    levels = ["n5", "n4", "n3", "n2", "n1"]

    if current_index >= len(kanji_deck) - 1:
        return handle_test_completion_or_advancement(request)

    current_kanji = Kanji.objects.get(id=kanji_deck[current_index])

    return render(request, 'level-test/kanji-test.html', {'kanji': current_kanji.expression, 'level': levels[int(request.session.get('current_level_index'))]})

def kanji_test_post(request):
    levels = ["n5", "n4", "n3", "n2", "n1"]

    current_index = int(request.session.get('current_index'))
    kanji_deck = request.session.get('kanji_deck', [])
    current_kanji = Kanji.objects.get(id=kanji_deck[current_index])
    level_up = False

    is_correct = check_answer_similarity(request.POST.get('answer').lower(), current_kanji.meaning)
    prev_kanji = current_kanji.expression
    correct_answer = current_kanji.meaning
    reading = current_kanji.reading


    current_level = levels[int(request.session.get('current_level_index'))]
    if is_correct:
        request.session['score'] += 1
        request.session['level_scores'][current_level] += 1

    # save information for post-test results
    request.session['correct'].append(is_correct)
    request.session['kanji'].append((prev_kanji, reading, current_level))
    request.session['correct_answers'].append(correct_answer)
    user_answer = request.POST.get('answer')
    request.session['user_answers'].append(user_answer)


    if current_index + 1 < len(kanji_deck):
        request.session['current_index'] += 1
        current_kanji = Kanji.objects.get(id=kanji_deck[int(request.session['current_index'])])
    else:
        request.session['current_index'] += 1
        level_up = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX request
        data = {
            'is_correct': is_correct,
            'prev_kanji': prev_kanji,
            'reading': reading,
            'correct_answer': correct_answer,
            'score': request.session['score'],
            'index': request.session['current_index'],
            'kanji': current_kanji.expression if not level_up else None,
            'level': levels[int(request.session.get('current_level_index'))],
            'level_up': level_up,
            'pass': True if request.session['score'] >= 5 else False,
        }
        response = JsonResponse(data)

    return response


def test_results(request):
    kanji_list = request.session.get('kanji', [])
    correct = request.session.get('correct', [])
    correct_answers = request.session.get('correct_answers', [])
    user_answers = request.session.get('user_answers', [])
    levels = ["n5", "n4", "n3", "n2", "n1"]
    level = levels[int(request.session.get('current_level_index'))]
    score = request.session.get('score', 0)
    level_scores = request.session.get('level_scores', {})

    # Create results list for the template
    results = []
    for index, (kanji_expression, kanji_reading, kanji_level) in enumerate(kanji_list):
        results.append((kanji_expression, kanji_reading, kanji_level, correct[index], user_answers[index], correct_answers[index]))

    context = {
        'results': results,
        'level': level,
        'score': score,
        'level_scores': level_scores
    }
    return render(request, 'level-test/test-results.html', context)

# def test_complete(request):
#     return render(request, 'level-test/test-complete.html', {'title': 'Test Complete'})
