from django.db import models
from django.contrib.auth.models import User

from geomap.models import Event

from django.utils import timezone
import datetime

import re
import codecs
import json
import pytz
import os

# flohmaerkte

filename = os.getcwd() + '/geomap/static/geomap/data/flohmaerkte.json'

wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

numberOfWeeks = 20

with open(filename) as data_file:    
    data = json.load(data_file)

if User.objects.filter(username="flohmaerkte"):
    user = User.objects.filter(username="flohmaerkte")[0]
else:
    user = User(username="flohmaerkte", password="flohmaerkte")
    user.save()

Event.objects.filter(user=user).delete()
now = datetime.datetime.now()

weekday_Today = now.isoweekday()
mondayMidnight = datetime.date(now.year,now.month,now.day) - datetime.timedelta(0, (weekday_Today-1)*24*60*60)
mondayMidnight = datetime.datetime.combine(mondayMidnight, datetime.time(0, 0, 0))

for flohmarkt in data['flohmaerkte']:
    if flohmarkt['Date'] in wochentage:
        weekday = wochentage.index(flohmarkt['Date'])
    
    else:
        weekday = int(raw_input("Value Error: " + flohmarkt['Date'] + ": "))
    
    hour = flohmarkt['Hour']
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
        event.eventType_subCategory = json.dumps(['fleemarket'])
        event.lng = float(flohmarkt['lng'])
        event.lat = float(flohmarkt['lat'])
        event.description = flohmarkt['Location']
        event.link = flohmarkt['link']
        creation_date = mondayMidnight + datetime.timedelta(days=weekday + n*7, hours = hours_Start)
        event.creation_date = creation_date.strftime('%Y-%m-%d %H:%M+0100')
        if len(hourEnd.split(".")) == 2:
            hours_End = int(hourEnd.split(".")[0]) + min(float(hourEnd.split(".")[1])/60,1) - hours_Start
        elif len(hourEnd.split(".")) == 1:
            hours_End = int(hourEnd.split(".")[0]) - hours_Start
        else:
            print("error" + hourEnd)
        valid_until = mondayMidnight + datetime.timedelta(days=weekday + n*7, hours = hours_Start) + datetime.timedelta(hours = hours_End)
        event.valid_until = valid_until.strftime('%Y-%m-%d %H:%M+0100')
        event.save()
    
