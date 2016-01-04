import pyproj
import folium
import json
from functools import partial

from shapely.geometry import Point, LineString, Polygon, mapping
from shapely.wkt import loads  
from shapely.ops import transform

# Function to transform the LonLat Coordinate System to a System with Meters
transformationScheme = partial(
    pyproj.transform,
    pyproj.Proj(init='EPSG:4326'),
    pyproj.Proj(init='EPSG:32632'))

transformationScheme_Reverse = partial(
    pyproj.transform,
    pyproj.Proj(init='EPSG:32632'),
    pyproj.Proj(init='EPSG:4326'))

def getPolygon(lat, lon, bufferDistance):
    point = Point(lon, lat)
    point_Transformed = transform(transformationScheme, point)
    poly_Transformed = point_Transformed.buffer(bufferDistance)
    poly = transform(transformationScheme_Reverse, poly_Transformed)
    
    return poly

def unionPolygons(polygon1, polygon2):
    return polygon1.union(polygon2)

def intersectPolygons(polygon1, polygon2):
    if polygon1 is None:
        return polygon2
    
    if polygon2 is None:
        return polygon1
    else:
        return polygon1.intersection(polygon2)

def extractCoordinates(poly):
    # Extract the point values that define the perimeter of the polygon
    x,y = poly.exterior.coords.xy
    
    polygon = list()
    for x_coordinate, y_coordinate in zip(x, y):
        polygon.append([y_coordinate, x_coordinate])
    return polygon


def saveGeoJSON(filename, geojson):
    f = open(filename, 'w')
    f.write(geojson)
    f.close()
    return