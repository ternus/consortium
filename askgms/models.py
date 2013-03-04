from django.db import models

# Create your models here.

class Question(models.Model):
    asker_email = models.EmailField(blank=True)
    public = models.BooleanField(default=False, blank=True)
    question = models.TextField()
    asked_on = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True)
    answered_by = models.CharField(max_length=256, blank=True)
    answered_on = models.DateTimeField(blank=True, null=True)