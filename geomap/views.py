from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from django.contrib.gis.db import models
from .models import Map, Choice

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry

import json

from makePolygons import *
from getGoogleData import *

from django.db import IntegrityError


def index(request):
    context = {}
    return render(request, 'geomap/index.html', context)

def loginUser(request):
    logout(request)
    error_message = ''
    if request.method == u'POST':
        POST = request.POST
        verificationCode = POST.get('verificationCode', False)
        username = POST.get('username', False)
        password = POST.get('password', False)
        if verificationCode == 'rivutec':
            user = authenticate(username=username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    return HttpResponseRedirect(reverse('geomap:detail', args=(1,)))
                else:
                    # Return a 'disabled account' error message
                    error_message = 'disabled account'
            else:
                try:
                    user = User.objects.create_user(username, password = password)
                    user.save()
                    user = authenticate(username=username, password = password)
                    login(request, user)
                    return HttpResponseRedirect(reverse('geomap:detail', args=(1,)))
                except IntegrityError:
                    error_message = 'IntegrityError'
        else:
            error_message = 'Wrong Verfication Code'
            
    return render_to_response('geomap/index.html', {'error_message': error_message}, context_instance=RequestContext(request))


def logoutUser(request):
    logout(request)
    context = {}
    return render(request, 'geomap/index.html', context)
    
@login_required
def detail(request, map_id):
    username = request.user.username
    map = get_object_or_404(Map, pk=map_id)
    choices_list = Choice.objects.filter(map = map)
    polygon_geoGESON = None
    
    if choices_list:
        polygon = choices_list[0].choice_polygon
        for choice in choices_list:
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
            'user' : username},)

@login_required
def addField(request, map_id):
    map = get_object_or_404(Map, pk=map_id)
    
    try:
        store = request.POST['store']
        radius = int(request.POST['radius'])
    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'geomap/detail.html', {
            'map': map,
            'error_message': "You didn't select a choice.",
            'choices_list' : choices_list,
        })
    else:
        
        results = queryGoogle_radarSearch(map.map_center_lat, map.map_center_lon, map.map_center_radius, store)
        polygon = getPolygonFromQuery(results, radius)
        
        if isinstance(GEOSGeometry(polygon.wkt), geos.Polygon):
            choice_polygon = geos.MultiPolygon(GEOSGeometry(polygon.wkt))
        else:
            choice_polygon = polygon.wkt
        
        choice = Choice(map=map, choice_text=store, choice_radius =  radius, choice_polygon = choice_polygon)
        choice.save()
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('geomap:detail', args=(map.id,)))
    

@login_required
def changeMap(request, map_id):
    response = {'status': 0, 'message': "Your error"} 
    map = get_object_or_404(Map, pk=map_id)
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
    
