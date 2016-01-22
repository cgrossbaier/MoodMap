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

# wochenmaerkte

filename = os.getcwd() + '/geomap/static/geomap/data/wochenmaerkte.json'

wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

numberOfWeeks = 20

localtimezone = pytz.timezone('Europe/Berlin')

with open(filename) as data_file:    
    data = json.load(data_file)

if User.objects.filter(username="wochenmaerkte"):
    user = User.objects.filter(username="wochenmaerkte")[0]
else:
    user = User(username="wochenmaerkte", password="wochenmaerkte")
    user.save()

Event.objects.filter(user=user).delete()
now = datetime.datetime.now()

weekday_Today = now.isoweekday()
mondayMidnight = datetime.date(now.year,now.month,now.day) - datetime.timedelta(0, (weekday_Today-1)*24*60*60)
mondayMidnight = datetime.datetime.combine(mondayMidnight, datetime.time(0, 0, 0))

for wochenmarkt in data['wochenmaerkte']:
    if wochenmarkt['Date'] in wochentage:
        weekday = wochentage.index(wochenmarkt['Date'])
    
    else:
        weekday = int(raw_input("Value Error: " + wochenmarkt['Date'] + ": "))
    
    hour = wochenmarkt['Hour']
    hourStart = hour.split()[0]
    hourEnd = hour.split()[2]
    if len(hourStart.split(".")) == 2:
        hours_Start = int(hourStart.split(".")[0]) + min(float(hourStart.split(".")[1])/60,1)
    elif len(hourStart.split(".")) == 1:
        hours_Start = int(hourStart.split(".")[0])
    else:
        print("error" + hourStart)
    for n in range(numberOfWeeks):
        event = Event()
        event.user = user
        event.eventType = 'event'
        event.eventType_subCategory = json.dumps(['wochenmaerkte'])
        event.lng = float(wochenmarkt['lng'])
        event.lat = float(wochenmarkt['lat'])
        event.description = wochenmarkt['Location']
        creation_date = localtimezone.localize(mondayMidnight + datetime.timedelta(days=weekday + n*7, hours = hours_Start))
        event.creation_date = creation_date.strftime('%Y-%m-%d %H:%M+0100')
        if len(hourEnd.split(".")) == 2:
            hours_End = int(hourEnd.split(".")[0]) + min(float(hourEnd.split(".")[1])/60,1) - hours_Start
        elif len(hourEnd.split(".")) == 1:
            hours_End = int(hourEnd.split(".")[0]) - hours_Start
        else:
            print("error" + hourEnd)
        event.valid_until = mondayMidnight + datetime.timedelta(days=weekday + n*7, hours = hours_Start) + datetime.timedelta(hours = hours_End)
        event.save()
    
