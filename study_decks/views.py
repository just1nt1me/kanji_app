from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from level_test.models import Kanji
from .models import UserKanjiProgress
from .utils import get_kanji_for_study, update_sm2_progress
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

def study(request):
    return render(request, 'study-decks/study.html')

@login_required
def study_level(request, jlpt_level):
    if request.method == 'POST':
        # Handle user feedback and update progress
        user_kanji_progress_id = request.POST.get('user_kanji_progress_id')
        feedback = request.POST.get('feedback')

        user_kanji_progress = UserKanjiProgress.objects.get(id=user_kanji_progress_id)
        update_sm2_progress(user_kanji_progress, feedback)

        return JsonResponse({'status': 'success'})

    # Fetch a kanji for study
    kanji_to_study = get_kanji_for_study(request.user, jlpt_level)
    if not kanji_to_study:
        # No kanji to study, redirect or show a message
        return render(request, 'no_kanji_to_study.html')

    context = {
        'kanji_to_study': kanji_to_study[0],  # Display one kanji at a time
        'jlpt_level': jlpt_level
    }
    return render(request, 'study-decks/study_level.html', context)
