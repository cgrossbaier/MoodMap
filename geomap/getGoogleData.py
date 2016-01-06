import urllib
import json

from makePolygons import *

## API KEY
key = "AIzaSyC_XaGJy5dpcH2YoYDckNv-IfCKIeiSNSU"

def queryGoogle_radarSearch(lat, lon, radius, types):
    googleGeocodeUrl = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?'
    url = googleGeocodeUrl + "location=" + str(lat) + "," + str(lon) + "&radius=" + str(radius) + "&keyword=" + types + "&key=" + key
    json_response = urllib.urlopen(url)
    response = json.loads(json_response.read())
    
    if response['results']:
        results = response['results']
    else:
        results = None
        print types, "<no results>"
    
    return results

    
def getPolygonFromQuery(results, bufferDistance):
    polygon = Point(0,0)
    polygon = polygon.buffer(0)
    for location in results:
        lat = location['geometry']['location']['lat']
        lon = location['geometry']['location']['lng']
        polygon = unionPolygons(polygon, getPolygon(lat, lon, bufferDistance))
    
    return polygon

