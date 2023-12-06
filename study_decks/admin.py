from django.contrib import admin
from .models import UserKanjiProgress
from level_test.models import Kanji

admin.site.register(Kanji)
admin.site.register(UserKanjiProgress)
