from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from django.contrib.gis.db import models
from .models import Map, Choice, Feedback

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry

import json

from makePolygons import *
from getGoogleData import *

from django.db import IntegrityError

from random import randint
import string


############### variables ###############

colours = ["#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf"]
numberOfColours = len(colours)

############### Pages ###############


def index(request):
    context = {}
    return render(request, 'geomap/index.html', context)


@login_required
def detail(request, map_id):
    username = request.user.username
    map = get_object_or_404(Map, pk=map_id)
    choices_list = Choice.objects.filter(map = map)
    polygon_geoGESON = None
    polygon_Choices_geoGESON = []
    polygon_Choices_colours = []
    
    if choices_list:
        polygon = choices_list[0].choice_polygon
        for choice in choices_list:
            polygon_Choices_geoGESON.append(choice.choice_polygon.geojson)
            polygon_Choices_colours.append(choice.choice_colour)
            
            polygon = intersectPolygons(polygon, choice.choice_polygon)

        polygon_geoGESON = polygon.geojson
                
        if GEOSGeometry(polygon.wkt).dims == -1:
            map.map_polygon = None
        
        else:
            if isinstance(GEOSGeometry(polygon.wkt), geos.Polygon):
                map.map_polygon = geos.MultiPolygon(GEOSGeometry(polygon.wkt))
            else:
                map.map_polygon = polygon.wkt
            
        map.save()
    
    return render(request, 'geomap/detail.html', {
            'map': map,
            'choices_list' : choices_list,
            'polygon' : polygon_geoGESON,
            'polygon_Choices_geoGESON' : polygon_Choices_geoGESON,
            'polygon_Choices_colours' : json.dumps(polygon_Choices_colours),
            'user' : username},)



@login_required
def feedback(request, map_id):
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
        return render(request, 'geomap/feedback.html', context)
        

############### Functions ###############

def loginUser(request):
    logout(request)
    error_message = ''
    if request.method == u'POST':
        POST = request.POST
        verificationCode = POST.get('verificationCode', False)
        NumberOfUsers = len(User.objects.all())+1
        username = makeSessionId(str(NumberOfUsers))
        password = 'user1234'
        if verificationCode == 'rivutec':
            try:
                user = User.objects.create_user(username, password = password)
                user.save()
                user = authenticate(username=username, password = password)
                login(request, user)

                # Create map for user
                map_user = Map()
                map_user.user = user
                map_user.map_title = 'Map'
                map_user.pub_date = timezone.now()
                map_user.map_center_lon = -0.101709365845
                map_user.map_center_lat = 51.5003012206
                map_user.map_center_radius = 2000
                map_user.map_center_zoom = 12

                map_user.save()
                
                choice_text = 'Thai food'
                choice_radius = 200
                choice_colour = colours[0]
                results = queryGoogle_radarSearch(map_user.map_center_lat, 
                                                  map_user.map_center_lon, 
                                                  map_user.map_center_radius, 
                                                  choice_text)
                
                if results is not None:
                    polygon = getPolygonFromQuery(results, int(choice_radius))

                    if isinstance(GEOSGeometry(polygon.wkt), geos.Polygon):
                        choice_polygon = geos.MultiPolygon(GEOSGeometry(polygon.wkt))
                    else:
                        choice_polygon = polygon.wkt

                    choice = Choice()
                    choice.map = map_user
                    choice.choice_text = choice_text
                    choice.choice_radius = choice_radius
                    choice.choice_polygon = choice_polygon
                    choice.choice_colour = choice_colour
                    choice.save()
                
                
                choice_text = 'Pub'
                choice_radius = 50
                choice_colour = colours[1]
                results = queryGoogle_radarSearch(map_user.map_center_lat, 
                                                  map_user.map_center_lon, 
                                                  map_user.map_center_radius, 
                                                  choice_text)
                
                if results is not None:
                    polygon = getPolygonFromQuery(results, int(choice_radius))

                    if isinstance(GEOSGeometry(polygon.wkt), geos.Polygon):
                        choice_polygon = geos.MultiPolygon(GEOSGeometry(polygon.wkt))
                    else:
                        choice_polygon = polygon.wkt

                    choice = Choice()
                    choice.map = map_user
                    choice.choice_text = choice_text
                    choice.choice_radius = choice_radius
                    choice.choice_polygon = choice_polygon
                    choice.choice_colour = choice_colour
                    choice.save()
                    
                return HttpResponseRedirect(reverse('geomap:detail', args=(map_user.id,)))
            except IntegrityError:
                error_message = 'User already exists'
        else:
            error_message = 'Wrong Verfication Code'
            
    return render_to_response('geomap/index.html', {'error_message': error_message}, context_instance=RequestContext(request))



@login_required
def logoutUser(request):
    logout(request)
    context = {}
    return HttpResponseRedirect(reverse('geomap:index', args=()))

@login_required
def addChoice(request, map_id):
    response = {'status': 'Not okay', 'message': 'No Post method'}
    map = get_object_or_404(Map, user=request.user)
    if request.method == u'POST':
        try:
            choice_text = request.POST['queryText']
            choice_radius = request.POST['queryRadius']
        except (KeyError):
            response = {'status': 'Not okay', 'message': 'KeyError'}
        else:
            # Make sure that values are correct
            if choice_text == "" or choice_radius == "" or int(choice_radius) <= 0:
                response = {'status': 'Not okay', 'message': 'Please adjust your query'}
            else:
                results = queryGoogle_radarSearch(map.map_center_lat, map.map_center_lon, map.map_center_radius, choice_text)
                
                if results is not None:
                    polygon = getPolygonFromQuery(results, int(choice_radius))

                    if isinstance(GEOSGeometry(polygon.wkt), geos.Polygon):
                        choice_polygon = geos.MultiPolygon(GEOSGeometry(polygon.wkt))
                    else:
                        choice_polygon = polygon.wkt
                        
                    numberOfChoices = len(Choice.objects.all())
                    choice = Choice()
                    choice.map = map
                    choice.choice_text = choice_text
                    choice.choice_radius = choice_radius
                    choice.choice_polygon = choice_polygon
                    choice.choice_colour = colours[((numberOfChoices + 1) % numberOfColours)]              
                    choice.save()
                    response = {'status': "Okay", 
                                'choice_id': choice.id,
                                'choice_text': choice.choice_text,
                                'choice_radius': choice.choice_radius,
                                'choice_polygon': choice.choice_polygon.geojson,
                                'choice_colour': choice.choice_colour} 
                else:
                    response = {'status': 'Not okay', 'message': 'Nothing found'}
            
            return HttpResponse(json.dumps(response), content_type='application/json')
    

@login_required
def changeMap(request, map_id):
    response = {'status': 0, 'message': "Your error"} 
#    map = get_object_or_404(Map, pk=map_id)
    map = get_object_or_404(Map, user=request.user)
    if request.method == u'POST':
        response = {'status': 2, 'message': "Post Request, no Data"} # for ok
        POST = request.POST
        changeType = POST.get('changeType', False)
        
        if changeType == 'changePosition':
            # Get lat coordinate
            lat = float(str(POST.get('lat')))
            # Get lon coordinate
            lon = float(str(POST.get('lon')))
            # Change Location of map
            map.map_center_lat = lat
            map.map_center_lon = lon
            response = {'status': "changedPosition", 'message': (map.map_center_zoom, map.map_center_lat, map.map_center_lon)}
        
        if changeType == 'changeZoom':
            # Get zoom
            zoom = float(str(POST.get('zoom')))
            map.map_center_zoom = zoom
            response = {'status': "changedZoom", 'message': (map.map_center_zoom, map.map_center_lat, map.map_center_lon)}
        
        if changeType == 'resetMap':
            # Get Map
            map = get_object_or_404(Map, pk=map_id)
            choices_list = Choice.objects.filter(map = map)
    
            if choices_list:
                for choice in choices_list:
                    choice.delete()
            
            map.map_polygon = None
            response = {'status': 'resetMap'}
            
        map.save()
        # for ok
        return HttpResponse(json.dumps(response), content_type='application/json')
    

@login_required
def changeChoice(request, map_id):
    response = {'status': 0, 'message': "No Post Request"} 
    map = get_object_or_404(Map, pk=map_id)
    if request.method == u'POST':
        POST = request.POST
        changeType = POST.get('changeType', False)
        
        if changeType == 'deleteChoice':
            # Get lat coordinate
            choiceID = str(POST.get('choiceID'))
            selectedChoice = Choice.objects.filter(id = choiceID)
            selectedChoice.delete()
            response = {'status': 'Choice deleted'} # for ok
        return HttpResponse(json.dumps(response), content_type='application/json')
    
@login_required
def saveFeedback(request, map_id):
    response = {'status': "Not Okay", 'message': "Please try again"} 
    user=request.user
    if request.method == u'POST':
        response = {'status': "Not Okay", 'message': "You didn't answer all the questions."}
        POST = request.POST
        feedbackGeneral = POST.get('feedbackGeneral', False)
        feedbackLiveData = POST.get('feedbackLiveData', False)
        feedbackProblems = POST.get('feedbackProblems', False)
        
        if feedbackGeneral != "" or feedbackLiveData != "" or feedbackProblems != "":
            response = {'status': "Not Okay", 'message': "Could you please write a little bit more."}
            if len(feedbackGeneral) >= 150 and len(feedbackLiveData) >= 150 and len(feedbackProblems) >= 150:
                feedback = Feedback()
                feedback.user = user
                feedback.generalFeedback = feedbackGeneral
                feedback.dataSource = feedbackLiveData
                feedback.problem = feedbackProblems
                feedback.save()
                response = {'status': "Okay"} 
    
    return HttpResponse(json.dumps(response), content_type='application/json')

    
def makeSessionId(st):
	import md5, time, base64
	m = md5.new()
	m.update('this is a test of the emergency broadcasting system')
	m.update(str(time.time()))
	m.update(str(st))
	return string.replace(base64.encodestring(m.digest())[:-3], '/', '$')


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
        answers = [u'%s' % (feedback.user.username), 
                   u'%s' % (feedback.generalFeedback),
                  u'%s' % (feedback.dataSource),
                  u'%s' % (feedback.problem)]
        writer.writerow(answers)
    
    return response

@login_required
def export_user(request):
    
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export_user.csv'
    
    # Delimiter ',' for German Excel
    writer = csv.writer(response, dialect=csv.excel, delimiter=';')
    column_list = ["MturkCode", "Choice Text", "Choice Radius"]
    writer.writerow(column_list)
    # List of Users
    users = User.objects.all().order_by('id')
    for user in users:
        map = Map.objects.filter(user=user)
        if map:
            choices = Choice.objects.filter(map=map[0]).order_by('id')
            for choice in choices:
                answers = [u'%s' % (map[0].user.username), 
                           u'%s' % (choice.choice_text),
                          u'%s' % (choice.choice_radius)]
                writer.writerow(answers)
    
    return response
