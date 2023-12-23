from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from level_test.models import Kanji
from .models import UserKanjiProgress
from .utils import initialize_kanji, get_kanji_for_study, update_sm2_progress
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('level-test-home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def study(request):
    return render(request, 'study-decks/study.html')

def study_level(request, jlpt_level):
    if request.method == 'POST':
        # Handle user feedback and update progress
        user_kanji_progress_id = request.POST.get('user_kanji_progress_id')
        feedback = request.POST.get('feedback')

        user_kanji_progress = UserKanjiProgress.objects.get(id=user_kanji_progress_id)
        update_sm2_progress(user_kanji_progress, feedback)

        # Fetch the next kanji for study after updating
        next_kanji_to_study = get_kanji_for_study(request.user, jlpt_level)

        if next_kanji_to_study:
            next_kanji_data = {
                'id': next_kanji_to_study[0].id,
                'expression': next_kanji_to_study[0].kanji.expression,
                'meaning': next_kanji_to_study[0].kanji.meaning,
                'reading': next_kanji_to_study[0].kanji.reading,
            }
            return JsonResponse({'next_kanji': next_kanji_data})
        else:
            return JsonResponse({'next_kanji': None})

    else:
        # Initialize kanji progress for the session if needed
        initialize_kanji(request.user, jlpt_level)

        # GET request: Render the initial study page
        kanji_to_study = get_kanji_for_study(request.user, jlpt_level)

        context = {
            'kanji_to_study': kanji_to_study[0] if kanji_to_study else None,
            'jlpt_level': jlpt_level
        }
        return render(request, 'study-decks/study_level.html', context)
