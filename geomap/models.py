from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventType = models.CharField(max_length=200)
    description = models.CharField(max_length=800)
    creation_date = models.DateTimeField('date published')
    valid_until = models.DateTimeField('date published')
    lng = models.FloatField()
    lat = models.FloatField()
    
    def __str__(self):
        return self.eventType
