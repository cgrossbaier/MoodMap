from django.db import models
from django.contrib.auth.models import User

from geomap.models import Event, Statistic, Feedback

from django.utils import timezone
import datetime

import re
import codecs
import json
import pytz
import os

#filename = '/Users/christophgrossbaier/Documents/rivutec/MoodMapDjango/venv/polizeireports.json'
filename = os.getcwd() + '/geomap/static/geomap/data/polizeireports.json'

# policreports
with open(filename) as data_file:    
    data = json.load(data_file)

if User.objects.filter(username="polizeireports"):
    user = User.objects.filter(username="polizeireports")[0]
else:
    user = User(username="polizeireports", password="police")
    user.save()

#Event.objects.filter(user=user).delete()

creation_date_max = Event.objects.filter(user=user).latest('creation_date').creation_date
localtimezone = pytz.timezone('Europe/Berlin')

for feature in data['features']:
    creation_date = localtimezone.localize(datetime.datetime.strptime(feature['properties']['date'], '%d.%m.%Y %H:%M'))
    if creation_date > creation_date_max:
        print('New Policereport')
        event = Event()
        event.user = user
        event.creation_date = datetime.datetime.strptime(feature['properties']['date'], '%d.%m.%Y %H:%M').strftime('%Y-%m-%d %H:%M+0100')
        event.eventType = 'info'
        event.eventType_subCategory = 'police'
        valid_until = datetime.datetime.strptime(feature['properties']['date'], '%d.%m.%Y %H:%M') + datetime.timedelta(hours = 23)
        event.valid_until = valid_until.strftime('%Y-%m-%d %H:%M+0100')
        event.lng = float(feature['geometry']['coordinates'][0])
        event.lat = float(feature['geometry']['coordinates'][1])
        event.description = feature['properties']['description']
        event.link = feature['properties']['link']   
        event.save()

