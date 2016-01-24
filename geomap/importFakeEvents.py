# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from geomap.models import Event, Statistic, Feedback

from django.utils import timezone
import datetime

import csv
import random
import pytz
import sys
import os
import json

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

#
#with open(filename, 'rb') as csvfile:
#    events = csv.reader(csvfile, delimiter=';')
#    next(events, None)  # skip the headers
#    for event in events:
#        newEvent = Event()
#        newEvent.user = user
#        newEvent.creation_date = timezone.now()
#        newEvent.eventType = event[0]
#        newEvent.eventType_subCategory = json.dumps(event[1].split("-"))
#        newEvent.valid_until = timezone.now() + datetime.timedelta(0, random.uniform(30.0, 240.0)*60)
#        newEvent.lng = random.uniform(lng_NW, lng_SE)
#        newEvent.lat = random.uniform(lat_SE, lat_NW)
#        newEvent.description = event[2]
#        newEvent.save()
#        print(event[0])
#        print(event[1])
#        print(event[2])
#        print('-------')

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

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

#
#import gdata.service
#import gdata.spreadsheet
#import gdata.spreadsheet.service
#import gdata.spreadsheet.text_db
#import logging
#import socket
#
#gd_client = gdata.spreadsheet.service.SpreadsheetsService()
#
## Set the email to your Google account email
#gd_client.email = 'c.grossbaier@gmail.com'
#
## Set the password to your Google account password. Please note that if you have
## enabled the 2-steps authentication in Google you will have to generate a
## password for this script.
#gd_client.password = 'uqtnbpjfphrjoymv'
#
#try:
#    gd_client.ProgrammaticLogin()
#except socket.sslerror, e:
#    logging.error('Spreadsheet socket.sslerror: ' + str(e))
#
## key: is the "key" value that you see in the url bar of the browser once you
## open a Google Docs spreadsheet
#key = '14TQhBxGoy-ur_3s-JANo2v8DZadK1YRbtaz5MBY_0k0'
#
## This is the worksheet ID: the default name of the first sheet is "od6"
#wksht_id = 'od6'
#
#try:
#    feed = gd_client.GetListFeed(key, wksht_id)
#except gdata.service.RequestError, e:
#    logging.error('Spreadsheet gdata.service.RequestError: ' + str(e))
#except socket.sslerror, e:
#    logging.error('Spreadsheet socket.sslerror: ' + str(e))
#
#for row_entry in feed.entry:
#    record = gdata.spreadsheet.text_db.Record(row_entry=row_entry)
#    print "%s,%s,%s" % (record.content['firstname'], record.content['lastname'], record.content['telephone'])
