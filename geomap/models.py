from __future__ import unicode_literals

from django.contrib.gis.db import models
from shapely.geometry import Point, LineString, Polygon, mapping

from django.contrib.gis import geos

from django.contrib.auth.models import User

# Create your models here.

class Map(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    map_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    map_center_lon = models.FloatField()
    map_center_lat = models.FloatField()
    map_center_radius = models.FloatField()
    map_center_zoom = models.FloatField()
    
    map_polygon = models.MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.map_title
    

class Choice(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    choice_radius = models.IntegerField()
    choice_polygon = models.MultiPolygonField(null=True)
    choice_colour = models.CharField(default='#377eb8', max_length=7)
    
    def __str__(self):
        return self.choice_text

class Feedback(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    generalFeedback = models.TextField(blank=True)
    dataSource = models.TextField(blank=True)
    problem = models.TextField(blank=True)
    def __str__(self):
        return 'User ' + str(self.user.id)
