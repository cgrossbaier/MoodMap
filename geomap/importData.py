from django.db import models
from django.contrib.auth.models import User

from geomap.models import Event, Statistic, Feedback

from django.utils import timezone
import datetime

import re
import codecs
import json

# policreports
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
    event.creation_date = datetime.datetime.strptime(feature['properties']['date'], '%d.%m.%Y %H:%M').strftime('%Y-%m-%d %H:%M+0100')
    event.eventType = 'info'
    event.eventType_subCategory = 'police'
    event.valid_until = datetime.datetime.strptime(feature['properties']['date'], '%d.%m.%Y %H:%M') + datetime.timedelta(hours = 24)
    event.lng = float(feature['geometry']['coordinates'][0])
    event.lat = float(feature['geometry']['coordinates'][1])
    event.description = feature['properties']['description']
    event.link = feature['properties']['link']   
    event.save()

    
# wochenmaerkte

wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

with open('/Users/christophgrossbaier/Documents/rivutec/MoodMapDjango/mysite/geomap/static/geomap/data/wochenmaerkte.json') as data_file:    
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
    event = Event()
    event.user = user
    event.eventType = 'event'
    event.eventType_subCategory = 'market'
    event.lng = float(wochenmarkt['lng'])
    event.lat = float(wochenmarkt['lat'])
    event.description = wochenmarkt['Location']
    
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
    
    creation_date = mondayMidnight + datetime.timedelta(days=weekday, hours = hours_Start)
    event.creation_date = creation_date.strftime('%Y-%m-%d %H:%M+0100')
    if len(hourEnd.split(".")) == 2:
        hours_End = int(hourEnd.split(".")[0]) + min(float(hourEnd.split(".")[1])/60,1) - hours_Start
    elif len(hourEnd.split(".")) == 1:
        hours_End = int(hourEnd.split(".")[0]) - hours_Start
    else:
        print("error" + hourEnd)
        
    event.valid_until = mondayMidnight + datetime.timedelta(days=weekday, hours = hours_Start) + datetime.timedelta(hours = hours_End)
    event.save()
        
events = Event.objects.filter(user=user)
with codecs.open('export_wochentage.csv', 'w', encoding='utf-8') as output:
    output.write('"eventType"; "eventType_subCategory"; "description"; "creation_date"; "valid_until"; "link"; "lng"; "lat"\n')
    for event in events:
        output.write('%s; %s; %s; %s; %s;%s;%s;%s;\n' % (event.eventType, event.eventType_subCategory, event.description, event.creation_date, event.valid_until, event.link, event.lng, event.lat))    
    
    
    
