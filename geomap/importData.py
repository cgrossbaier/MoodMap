from django.db import models
from django.contrib.auth.models import User

from geomap.models import Event, Statistic, Feedback

from django.utils import timezone
import datetime

import json

with open('/Users/christophgrossbaier/Documents/rivutec/MoodMapDjango/mysite/geomap/static/geomap/data/polizeireports.json') as data_file:    
    data = json.load(data_file)

user = User(username="polizeireports", password="police")
user.save()
    
for feature in data['features']:
    event = Event()
    event.user = user
    event.creation_date = timezone.now()
    event.eventType = 'warning'
    event.valid_until = timezone.now() + datetime.timedelta(0, int(50)*60)
    event.lng = float(feature['geometry']['coordinates'][0])
    event.lat = float(feature['geometry']['coordinates'][1])
    event.description = feature['properties']['title']            
    event.save()
