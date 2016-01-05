from django.contrib.auth.models import User

User.objects.filter(username="admin").delete()
user = User.objects.create_superuser("admin", "admin@admin.com", "admin")
user.save()

from django.contrib.gis.db import models
from geomap.models import Map, Choice
from django.utils import timezone

map_title = 'First Map'
pub_date = timezone.now()
map_center_lon = 50
map_center_lat = 0
map_center_radius = 2000
map_center_zoom = 14

map1 = Map(map_title = map_title, pub_date = pub_date, map_center_lon = map_center_lon, map_center_lat = map_center_lat, map_center_radius = map_center_radius, map_center_zoom = map_center_zoom)
map1.save()
