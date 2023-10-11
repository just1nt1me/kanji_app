from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Kanji, JLPTLevel
from .forms import KanjiTestForm
from .util import wordnet_similarity
from django.http import JsonResponse

# return what we want user to see from "home" page
def home(request):
    return render(request, 'level-test/home.html')

def about(request):
    return render(request, 'level-test/about.html', {'title': 'About'})

def kanji_test(request):
    n5_kanji = Kanji.objects.filter(tags__level='n5')[:10]
    context = {'kanji_list': n5_kanji}

    if request.method == 'POST':
        form = KanjiTestForm(request.POST)
        if form.is_valid():
            current_index = form.cleaned_data.get('current_index')
            user_answer = form.cleaned_data.get('answer')

            if current_index < len(n5_kanji):
                kanji = n5_kanji[current_index]
                correct_answer = kanji.meaning
                is_correct = form.is_answer_correct(correct_answer)

                form.fields['answer'].widget.attrs['class'] = 'correct' if is_correct else 'incorrect'
                current_index += 1
                form.cleaned_data['current_index'] = current_index  # increment the current index for the next kanji

                # If the request is AJAX, return the result in JSON format
                if request.is_ajax():
                    return JsonResponse({
                        'is_correct': is_correct,
                        'correct_answer': None if is_correct else correct_answer
                    })

                if is_correct:
                    context['correct_answer'] = None
                else:
                    context['correct_answer'] = correct_answer

                context['form'] = form  # Remember to include the form in the context
                return render(request, 'level-test/kanji-test.html', context)

    else:
        form = KanjiTestForm()

    context['form'] = form  # Adding the form to the context outside the POST block
    return render(request, 'level-test/kanji-test.html', context)
