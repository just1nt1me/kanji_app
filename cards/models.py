from django.db import models

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)

# class JLPTLevel(models.Model):
#     level = models.CharField(max_length=10)

class Card(models.Model):
    expression = models.CharField(max_length=100)
    reading = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    tags = models.TextField(max_length=10)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.expression
