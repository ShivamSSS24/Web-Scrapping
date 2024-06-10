from django.db import models
import os
from django.conf import settings

settings.configure(
    DEBUG=True,

    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        ...
    ]
)


class Job(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    job = models.ForeignKey(Job, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='PENDING')
    output = models.JSONField(null=True, blank=True)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
