from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    # on_delete = models.CASCADE when user was deleted tasks will also be deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_task = models.DateTimeField()
    date_task_created = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=80)
    text = models.TextField(max_length=400)
    is_done = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return self.title
