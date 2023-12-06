from django.db import models
from level_test.models import Kanji
from django.contrib.auth.models import User

class UserKanjiProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    last_reviewed = models.DateField(auto_now=True)
    next_review = models.DateField()
    repetition = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=0)  # Days until next review
