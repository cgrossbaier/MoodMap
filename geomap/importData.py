from django.db import models
from django.contrib.auth.models import User

from geomap.models import Event, Statistic, Feedback

from django.utils import timezone
import datetime

import json

with open('/Users/christophgrossbaier/Documents/rivutec/MoodMapDjango/mysite/geomap/static/geomap/data/polizeireports.json') as data_file:    
    data = json.load(data_file)

if User.objects.filter(username="polizeireports"):
    user = User.objects.filter(username="polizeireports")[0]
else:
    user = User(username="polizeireports", password="police")
    user.save()

Event.objects.filter(user=user).delete()
    
for feature in data['features']:
    event = Event()
    event.user = user
    event.creation_date = datetime.datetime.strptime(feature['properties']['date'], '%d.%m.%Y %H:%M').strftime('%Y-%m-%d %H:%M')
    event.eventType = 'info'
    event.eventType_subCategory = 'police'
    event.valid_until = timezone.now() + datetime.timedelta(0, int(50)*60)
    event.lng = float(feature['geometry']['coordinates'][0])
    event.lat = float(feature['geometry']['coordinates'][1])
    event.description = feature['properties']['title']
    event.link = feature['properties']['link']   
    event.save()
