from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventType = models.CharField(max_length=200)
    eventType_subCategory = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=800, default="")
    creation_date = models.DateTimeField('date published')
    valid_until = models.DateTimeField('date published')
    link = models.CharField(max_length=400, default="", blank=True)
    lng = models.FloatField()
    lat = models.FloatField()
    
    def isActive(self):
        return self.valid_until >= timezone.now() and timezone.now() >= self.creation_date
    
    def __str__(self):
        return self.eventType
    
class Feedback(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    feedback1 = models.TextField(blank=True)
    feedback2 = models.TextField(blank=True)
    feedback3 = models.TextField(blank=True)
    feedback4 = models.TextField(blank=True)
    feedback5 = models.TextField(blank=True)
    def __str__(self):
        return 'User ' + str(self.user.id)

class Statistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    statType = models.CharField(max_length=200)
    timestamp = models.DateTimeField('date published')
    lng = models.FloatField()
    lat = models.FloatField()
    zoom = models.FloatField()
    
    def __str__(self):
        return self.statType