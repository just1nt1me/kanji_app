from datetime import date, timedelta
from level_test.models import Kanji
from .models import UserKanjiProgress

def get_kanji_for_study(user, jlpt_level):
    # Get all kanji for the specified JLPT level
    kanji = Kanji.objects.filter(jlpt_level=jlpt_level)

    # Get or create user progress for these kanji
    for k in kanji:
        progress, created = UserKanjiProgress.objects.get_or_create(
            user=user,
            kanji=k,
            defaults={'next_review': date.today()}
        )
        if created:
            # If the progress record is newly created, set the next review to today
            progress.next_review = date.today()
            progress.save()

    # Select kanji based on the next review date
    kanji_to_study = UserKanjiProgress.objects.filter(
        user=user,
        kanji__jlpt_level=jlpt_level,
        next_review__lte=date.today()
    ).order_by('next_review')[:10]  # Limit to 10 kanji for the session

    return kanji_to_study

# Updated function to match user feedback ("Again", "Hard", "Good", "Easy") to quality scores
def update_sm2_progress(user_kanji_progress, feedback):
    quality_map = {
        'Again': 0,
        'Hard': 1,
        'Good': 2,
        'Easy': 3
    }
    quality = quality_map.get(feedback, 0)  # Default to 0 if feedback is not recognized

    if quality < 2:
        user_kanji_progress.repetition = 0
        user_kanji_progress.interval = 1
    else:
        user_kanji_progress.repetition += 1
        if user_kanji_progress.repetition == 1:
            user_kanji_progress.interval = 1
        elif user_kanji_progress.repetition == 2:
            user_kanji_progress.interval = 6
        else:
            user_kanji_progress.interval = int(user_kanji_progress.interval * user_kanji_progress.ease_factor)

        # Adjust ease factor
        user_kanji_progress.ease_factor = max(1.3, user_kanji_progress.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

    user_kanji_progress.last_reviewed = date.today()
    user_kanji_progress.next_review = date.today() + timedelta(days=user_kanji_progress.interval)
    user_kanji_progress.save()
