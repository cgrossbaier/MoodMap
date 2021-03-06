from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from django.db import models
from .models import Event, Statistic, Feedback

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import urllib
import json
import googlemaps

from django.db import IntegrityError

from random import randint
import string
import datetime
import pytz

############### variables ###############

colours = ["#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf"]
numberOfColours = len(colours)

############### Pages ###############

def index(request):
    """
    index:
	The Login page
	"""
    context = {}
    return render(request, 'geomap/index.html', context)

def checkVerification(request):
    """
	checkVerification: 
    Check if verification Code is okay, then create user and call mapView function
	"""
    logout(request)
    error_message = 'No Post Method'
    if request.method == u'POST':
        POST = request.POST
        verificationCode = POST.get('verificationCode', False)
        NumberOfUsers = len(User.objects.all())+1
        username = makeSessionId(str(NumberOfUsers))
        password = 'user1234'
        if NumberOfUsers < 100:
            if verificationCode == 'MTURK_CODE':
                try:
                    user = User.objects.create_user(username, password = password)
                    user.save()
                    user = authenticate(username=username, password = password)
                    login(request, user)
                    return HttpResponseRedirect(reverse('geomap:mapView'))
                except IntegrityError:
                    error_message = 'User already exists'
            else:
                error_message = 'Wrong Verfication Code'
        else:
            error_message = 'Experiment is not running anymore.'
            
    return render_to_response('geomap/index.html', {'error_message': error_message}, context_instance=RequestContext(request))


@login_required
def mapView(request):
    """
    mapView
	Get all the events that are active and pass them over to the map function
	"""
    error_message = ""
    return render(request, 'geomap/map.html', {
            'error_message': error_message
            },)


@login_required
def addEvent(request):
    response = {'status': 'Not okay', 'message': 'No Post method'}
    if request.method == u'POST':
        try:
            eventType = request.POST['eventType']
            eventType_subCategory = request.POST['eventType_subCategory']
            valid_until = request.POST['valid_until']
            lng = request.POST['lng']
            lat = request.POST['lat']
            user_lng = request.POST['user_lng']
            user_lat = request.POST['user_lat']
            description = request.POST['description']
        except (KeyError):
            response = {'status': 'Not okay', 'message': 'KeyError'}
        else:
            event = Event()
            event.user = request.user
            event.creation_date = timezone.now()
            event.eventType = eventType
            event.eventType_subCategory = json.dumps(eventType_subCategory.split(","))
            event.valid_until = timezone.now() + datetime.timedelta(0, int(valid_until)*60)
            event.lng = float(lng)
            event.lat = float(lat)
            event.description = description             
            event.save()
            response = {'status': 'Okay',
                        'message': 'Event saved'}
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def searchQuery(request):
    response = {'status': 'Not okay', 'message': 'No Post method'}
    if request.method == u'POST':
        try:
            searchQuery = request.POST['searchQuery']
            boundNorthWest_lat = request.POST['boundNorthWest_lat']
            boundNorthWest_lng = request.POST['boundNorthWest_lng']
            boundSouthEast_lat = request.POST['boundSouthEast_lat']
            boundSouthEast_lng = request.POST['boundSouthEast_lng']
        except (KeyError):
            response = {'status': 'Not okay', 'message': 'KeyError'}
        else:
            lat, lng = queryGoogle_geocode(searchQuery,
                                          boundNorthWest_lat,
                                          boundNorthWest_lng,
                                          boundSouthEast_lat,
                                          boundSouthEast_lng);
            if (lat is not None and lng is not None):
                response = {'status': 'Okay', 
                            'lat': lat,
                            'lng': lng}
            else:
                response = {'status': 'Place not found', 'message': 'No result'}
    return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def updateEventList(request):
    response = {'status': 'Not okay', 'message': 'No Post method'}
    eventList = []
    eventListJson = {}
    if request.method == u'POST':
        try:
            lat_NW = float(request.POST['lat_NW'])
            lng_NW = float(request.POST['lng_NW'])
            lat_SE = float(request.POST['lat_SE'])
            lng_SE = float(request.POST['lng_SE'])
            user_lat = float(request.POST['user_lat'])
            user_lng = float(request.POST['user_lng'])
        except (KeyError):
            response = {'status': 'Not okay', 'message': 'KeyError'}
        else:
            eventListJson, eventList = getEvents(lat_NW, lng_NW, lat_SE, lng_SE, user_lat, user_lng)
        event_geoJSON = getGeoJSON(eventList)
        response = {'status': 'Okay',
                        'message': 'Event saved',
                        'event_geoJSON': event_geoJSON,
                       'eventListJson': json.dumps(eventListJson)}
    return HttpResponse(json.dumps(response), content_type='application/json')

def getEvents(lat_NW, lng_NW, lat_SE, lng_SE, user_lat, user_lng):
    events = Event.objects.all().order_by('-creation_date')
    eventListJson = []
    eventList = []
    for event in events:
        if event.isActive():
            if event.lat <= lat_NW and event.lat >= lat_SE and event.lng >= lng_NW and event.lng <= lng_SE:
                eventJson = {}
                timeDelta = timezone.now() - event.creation_date
                categories = set()
                if event.eventType_subCategory != "":
                    jsonDec = json.decoder.JSONDecoder()
                    subCategories = jsonDec.decode(event.eventType_subCategory)
                    for subCategory in subCategories:
                        categories.add(subCategory)
                if categories:
                    eventJson["eventType_subCategory"] = list(categories)
                else:
                    eventJson["eventType_subCategory"] = ""
                eventJson["eventType"] = event.eventType
                eventJson["lat"] = event.lat
                eventJson["lng"] = event.lng
                eventJson["duration"] = str(queryGoogle_walkingDistance(user_lat, user_lng, event.lat, event.lng))
                eventJson["description"] = event.description
                eventListJson.append(eventJson)
                eventList.append(event)
    return eventListJson, eventList

@login_required
def feedback(request):
    context = {}
    return render(request, 'geomap/feedback.html', context)

@login_required
def finalize(request):
    context = {}
    user = request.user
    if Feedback.objects.filter(user=user):
        context = {'username': request.user.username}
        logout(request)
        return render(request, 'geomap/finalize.html', context)
    else:
        return render(request, 'geomap/index.html', context)

############### Functions ###############

@login_required
def saveStatistics(request):
    response = {'status': 'Not okay', 'message': 'No Post method'}
    if request.method == u'POST':
        try:
            statType = request.POST['statType']
            lng = request.POST['lng']
            lat = request.POST['lat']
            zoom = request.POST['zoom']
        except (KeyError):
            response = {'status': 'Not okay', 'message': 'KeyError'}
        else:
            statistic = Statistic()
            statistic.user = request.user
            statistic.statType = statType
            statistic.timestamp = timezone.now()
            statistic.lng = float(lng)
            statistic.lat = float(lat)
            statistic.zoom = float(zoom)             
            statistic.save()
            response = {'status': 'Okay', 'message': 'Event saved'}
    return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def getCategories(request):
    response = {'status': 'Not okay', 'message': 'No Post method'}
    if request.method == u'POST':
        try:
            eventType = request.POST['eventType']
        except (KeyError):
            response = {'status': 'Not okay', 'message': 'KeyError'}
        else:
            events = Event.objects.all().filter(eventType=eventType)
            categories = set()
            jsonDec = json.decoder.JSONDecoder()
            for event in events:
                if event.eventType_subCategory != "":
                    subCategories = jsonDec.decode(event.eventType_subCategory)
                    for subCategory in subCategories:
                        categories.add(subCategory)
            value = 1
            category_List = []
            for category in categories:
                category_List.append({'text': category, 'value': category})
                value = value + 1
            if category_List:
                response = {'status': 'Okay', 'categories': json.dumps(category_List)}
            else:
                response = {'status': 'Okay', 'categories': ""}
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def saveFeedback(request):
    response = {'status': "Not Okay", 'message': "Please try again"} 
    user=request.user
    if request.method == u'POST':
        response = {'status': "Not Okay", 'message': "You didn't answer all the questions."}
        POST = request.POST
        feedback1 = POST.get('feedback1', False)
        feedback2 = POST.get('feedback2', False)
        feedback3 = POST.get('feedback3', False)
        
        if feedback1 != "" or feedback2 != "" or feedback3 != "":
            response = {'status': "Not Okay", 'message': "Could you please write a little bit more."}
            if len(feedback1) >= 150 and len(feedback2) >= 150 and len(feedback3) >= 150:
                feedback = Feedback()
                feedback.user = user
                feedback.feedback1 = feedback1
                feedback.feedback2 = feedback2
                feedback.feedback3 = feedback3
                feedback.save()
                response = {'status': "Okay"} 
    
    return HttpResponse(json.dumps(response), content_type='application/json')

def queryGoogle_geocode(searchQuery, boundNorthWest_lat, boundNorthWest_lng, boundSouthEast_lat,  boundSouthEast_lng):
    ## API KEY
    key = "AIzaSyC_XaGJy5dpcH2YoYDckNv-IfCKIeiSNSU"
    googleGeocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?'
    url = googleGeocodeUrl + "address=" + str(searchQuery) + "&bounds=" + boundNorthWest_lat + " " + boundNorthWest_lng + "|" + boundSouthEast_lat + " " + boundSouthEast_lng + " " + "&key=" + key
    json_response = urllib.urlopen(url)
    response = json.loads(json_response.read())

    if response['results']:
        result = response['results'][0]
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
    else:
        result = None
        lat = None
        lng = None
    return lat, lng

def queryGoogle_walkingDistance(start_lat, start_lng, stop_lat, stop_lng):
    ## API KEY
    gmaps = googlemaps.Client(key='AIzaSyCCx9Ielmj6w1F0N1KmPVdv77uNDdRpG1I')
    directions_result = gmaps.directions(str(start_lat)+"," + str(start_lng),
                                         str(stop_lat)+"," + str(stop_lng),
                                         mode="walking")
    duration = ""
    if directions_result[0]['legs'][0]:
        duration = directions_result[0]['legs'][0]['duration']['text']
    return duration

# Help Function
def makeSessionId(st):
	import md5, time, base64
	m = md5.new()
	m.update('this is a test of the emergency broadcasting system')
	m.update(str(time.time()))
	m.update(str(st))
	return string.replace(base64.encodestring(m.digest())[:-3], '/', '$')


def getMarkterStyle(event):
    eventType = event.eventType
    eventType_subCategory = ''
    if event.eventType_subCategory:
        jsonDec = json.decoder.JSONDecoder()
        if event.eventType_subCategory != "":
            eventType_subCategory = jsonDec.decode(event.eventType_subCategory)
    if eventType == 'danger':
        markerColor = "#e41a1c"
        markerSymbol = "d"
        if 'police' in eventType_subCategory:
            markerSymbol = "police"
    elif eventType == 'sales':
        markerColor = "#377eb8"
        markerSymbol = "star"
        if 'fleemarket' in eventType_subCategory:
            markerSymbol = "grocery"
        if 'wochenmaerkte' in eventType_subCategory:
            markerSymbol = "grocery"
    elif eventType == 'lovely':
        markerColor = "#4daf4a"
        markerSymbol = "heart"
    elif eventType == 'clean':
        markerColor = "#ff7f00"
        markerSymbol = "r"
    elif eventType == 'mobility':
        markerColor = "#ffff33"
        markerSymbol = "bus"
    elif eventType == 'event':
        markerColor = "#984ea3"
        markerSymbol = "music"
    else:
        markerColor = "#000000"
        markerSymbol = "b"
    return markerColor, markerSymbol


def getPopup(event, date_Start, date_End):
    popup = "<b>%s</b><br>%s - %s" % (event.eventType.title(), date_Start, date_End)

    if event.description != "":
        popup = popup + "<br>%s" % (event.description)
    if event.link != "":
        popup = popup + "<br><a href='%s' target='_blank'>Link</a>" % (event.link)
        
    jsonDec = json.decoder.JSONDecoder()
    button = ""
    if event.eventType_subCategory != "":
        subCategories = jsonDec.decode(event.eventType_subCategory)
        for subCategory in subCategories:
            button = button + "<div class='tags'>%s</div>" % (subCategory)
        popup = popup + "<div class='popup-tags'>%s</div>" % (button)

    return popup
        
def getGeoJSON(events):
    localtimezone = pytz.timezone('Europe/Berlin')
    markerSize = "small"
    events_GeoJSON = '{"type": "FeatureCollection", "features": ['
    notFirstElement = False
    for event in events:
        markerColor, markerSymbol = getMarkterStyle(event)
        date_Start = event.creation_date.astimezone(localtimezone).strftime('%d.%m.%Y %H:%M')
        date_End = event.valid_until.astimezone(localtimezone).strftime('%H:%M')
        popup = getPopup(event, date_Start, date_End)
        if notFirstElement:
            events_GeoJSON = events_GeoJSON + ','
        events_GeoJSON = events_GeoJSON + '{"type": "Feature", "geometry": { "type": "Point", '
        events_GeoJSON = events_GeoJSON + '"coordinates": [%s, %s]},' % (event.lng, event.lat)
        events_GeoJSON = events_GeoJSON + '"properties": {'
        events_GeoJSON = events_GeoJSON + '"date": "%s", "description": "%s","link": "%s","marker-color": "%s","marker-size": "%s","marker-symbol": "%s","popup": "%s"}}' % (date_Start, event.description, event.link, markerColor, markerSize, markerSymbol, popup)
        notFirstElement = True
    events_GeoJSON = events_GeoJSON + "]}"
    return events_GeoJSON

@login_required
def export_stats(request):
    
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export_stats.csv'
    
    # Delimiter ',' for German Excel
    writer = csv.writer(response, dialect=csv.excel, delimiter=';')
    column_list = ["User", "statType", "timestamp", "lng", "lat", "zoom"]
    writer.writerow(column_list)
    # List of Users
    users = User.objects.all().order_by('id')
    for user in users:
        statistics = Statistic.objects.filter(user=user)
        if statistics:
            for statistic in statistics:
                answers = [u'%s' % (user.username.encode('utf-8')), 
                           '%s' % (statistic.statType.encode('utf-8')),
                           u'%s' % (statistic.timestamp),
                           u'%s' % (statistic.lng),
                           u'%s' % (statistic.lat),
                           u'%s' % (statistic.zoom)]
                writer.writerow(answers)
    
    return response
    
@login_required
def export_feedback(request):
    
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export_feedback.csv'
    
    # Delimiter ',' for German Excel
    writer = csv.writer(response, dialect=csv.excel, delimiter=';')
    column_list = ["MturkCode", "General", "Problem", "Data source"]
    writer.writerow(column_list)
    # List of Users
    feedbacks = Feedback.objects.all().order_by('id')
    for feedback in feedbacks:
        answers = [(feedback.user.username.encode('utf-8')), 
                   (feedback.feedback1.encode('utf-8')),
                  (feedback.feedback2.encode('utf-8')),
                  (feedback.feedback3.encode('utf-8'))]
        writer.writerow(answers)
    
    return response

@login_required
def export_events(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export_events.csv'
    
    # Delimiter ';' for German Excel
    writer = csv.writer(response, dialect=csv.excel, delimiter=';')
    column_list = ["User", "eventType", "eventType_subCategory", "description", "creation_date", "valid_until", "lng", "lat"]
    writer.writerow(column_list)
    # List of Users
    users = User.objects.all().order_by('id')
    for user in users:
        events = Event.objects.filter(user=user)
        if events:
            for event in events:
                answers = [u'%s' % (user.username), 
                           '%s' % (event.eventType.encode('utf-8')),
                           '%s' % (event.eventType_subCategory.encode('utf-8')),
                           '%s' % (event.description.encode('utf-8')),
                           u'%s' % (event.creation_date),
                           u'%s' % (event.valid_until),
                           u'%s' % (event.lng),
                          u'%s' % (event.lat)]
                writer.writerow(answers)
    
    return response
