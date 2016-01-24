# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from geomap.models import Event, Statistic, Feedback

from django.utils import timezone
import datetime

import random
import pytz
import os
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

# fake events

lat_NW = 52.675499
lng_NW = 13.0884
lat_SE = 52.33812
lng_SE = 13.76134

filename = os.getcwd() + '/geomap/static/geomap/data/events.csv'

localtimezone = pytz.timezone('Europe/Berlin')

if User.objects.filter(username="admin"):
    user = User.objects.filter(username="admin")[0]
else:
    user = User(username="admin", password="admin")
    user.save()

filename = os.getcwd() + '/geomap/static/geomap/data/Moodmap-6137ab05624c.json'

json_key = json.load(open(filename))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)

wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/14TQhBxGoy-ur_3s-JANo2v8DZadK1YRbtaz5MBY_0k0/edit#gid=0").sheet1

events = wks.get_all_records()

for event in events:
    newEvent = Event()
    newEvent.user = user
    newEvent.creation_date = timezone.now()
    newEvent.eventType = event['eventType']
    newEvent.eventType_subCategory = json.dumps(event["eventType_subCategory"].split("-"))
    newEvent.valid_until = timezone.now() + datetime.timedelta(0, random.uniform(30.0, 240.0)*60)
    newEvent.lng = random.uniform(lng_NW, lng_SE)
    newEvent.lat = random.uniform(lat_SE, lat_NW)
    newEvent.description = event["description"]
    newEvent.save()
    print(event['eventType'])
    print(event["eventType_subCategory"])
    print(event["description"])
    print('-------')
