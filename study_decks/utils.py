from datetime import date, timedelta
from django.db.models import Min
from level_test.models import Kanji
from .models import UserKanjiProgress
import random
from django.db import transaction

def initialize_kanji(user, jlpt_level, num_kanji_needed=20):
    # Start a transaction to ensure database integrity
    with transaction.atomic():
        # Find out how many kanji progress records already exist for this user and level
        existing_progress_count = UserKanjiProgress.objects.filter(
            user=user,
            kanji__jlpt_level=jlpt_level,
        ).count()

        # Calculate how many new kanji progress records are needed for this session
        kanji_to_initialize = num_kanji_needed - existing_progress_count

        # If additional kanji progress records are needed, create them
        if kanji_to_initialize > 0:
            # Get the kanji for which the user does not have progress records yet
            kanji_ids_with_progress = UserKanjiProgress.objects.filter(
                user=user,
                kanji__jlpt_level=jlpt_level,
            ).values_list('kanji_id', flat=True)

            kanji_without_progress = Kanji.objects.filter(
                jlpt_level=jlpt_level
            ).exclude(id__in=kanji_ids_with_progress)[:kanji_to_initialize]

            # Create progress records for the needed number of kanji
            progress_list = [
                UserKanjiProgress(
                    user=user,
                    kanji=kanji_item,
                    last_reviewed=None,  # No review date set for new records
                    next_review=date.today(),  # Set the review date to today
                    # Set other fields as needed
                )
                for kanji_item in kanji_without_progress
            ]

            UserKanjiProgress.objects.bulk_create(progress_list)



def get_kanji_for_study(user, jlpt_level):
    # Get kanji that have been studied and are due for review
    reviewed_kanji = UserKanjiProgress.objects.filter(
        user=user,
        kanji__jlpt_level=jlpt_level,
        next_review__lte=date.today(),
        last_reviewed__isnull=False  # This will only include kanji that have been reviewed
    ).order_by('next_review')[:20]

    # If there are fewer than 20 reviewed kanji, fill the rest with unreviewed kanji
    if reviewed_kanji.count() < 20:
        remaining_slots = 20 - reviewed_kanji.count()
        unreviewed_kanji = UserKanjiProgress.objects.filter(
            user=user,
            kanji__jlpt_level=jlpt_level,
            last_reviewed__isnull=True  # This will include kanji that have not been reviewed
        )[:remaining_slots]

        kanji_to_study = list(reviewed_kanji) + list(unreviewed_kanji)
    else:
        kanji_to_study = reviewed_kanji

    kanji_to_study_list = list(kanji_to_study)
    random.shuffle(kanji_to_study_list)

    return kanji_to_study_list

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
