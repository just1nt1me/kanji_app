from django.db import models
from level_test.models import Kanji
from django.contrib.auth.models import User

class UserKanjiProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    last_reviewed = models.DateField(auto_now_add=True)
    next_review = models.DateField()
    proficiency_level = models.IntegerField(default=0)  # You can customize this based on your spaced repetition algorithm

    def __str__(self):
        return f"{self.user.username} - {self.kanji.character}"
