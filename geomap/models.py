from __future__ import unicode_literals

from django.contrib.gis.db import models

from shapely.geometry import Point, LineString, Polygon, mapping

from django.contrib.gis import geos

# Create your models here.

class Map(models.Model):
    map_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    map_center_lon = models.FloatField()
    map_center_lat = models.FloatField()
    map_center_radius = models.FloatField()
    map_center_zoom = models.FloatField()
    
    map_polygon = models.MultiPolygonField(null=True)

    def __str__(self):
        return self.map_title
    
#    def save(self, *args, **kwargs):
#        # if map_polygon ends up as a Polgon, make it into a MultiPolygon
#        if self.map_polygon and isinstance(self.map_polygon, geos.Polygon):
#            self.map_polygon = geos.MultiPolygon(self.map_polygon)
#            
#        self.save(*args, **kwargs)
    

class Choice(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    choice_radius = models.IntegerField()
    choice_polygon = models.MultiPolygonField(null=True)
    
    def __str__(self):
        return self.choice_text
