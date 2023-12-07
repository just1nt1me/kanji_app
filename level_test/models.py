from django.db import models

# class JLPTLevel(models.Model):
#     level = models.CharField(max_length=10)

class Kanji(models.Model):
    expression = models.TextField()
    reading = models.TextField()
    meaning = models.TextField()
    jlpt_level = models.CharField(max_length=10)
