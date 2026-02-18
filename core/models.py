import uuid
from django.db import models
from django.utils import timezone

def generate_token():
    return uuid.uuid4().hex

class Survey(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    order = models.IntegerField(default=0)

class Recipient(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=64, default=generate_token, unique=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(null=True, blank=True)

class Response(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("recipient", "question")
