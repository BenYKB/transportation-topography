import map_methods
import googlemaps
from datetime import datetime
import numpy as np
import math

MAX_STATIC_MAP_SIZE = 640

def data(address, radius, mode, grid=5):
    ''' Gets x, y and z data related to travel times to locations 
    in specified radius from a specified location.

    :param address: A string specifying street address, city, 
                    province and/or country. Example:
                    '4700 Kingsway, Burnaby, BC'

    :param radius: A float in kilometers specifying the radius from
                   the address to map.

    :param mode: A string. "driving", "walking", "bicycling", 
                 or "transit"

    :param grid: Spacing of grid. Default is 5

    :rtype: X, Y, Z. If N = grid value,
            X: N length array of longitude values
            Y: N length array of latitude values
            Z: NxN array of travel times
    '''

    key_file = open("key.txt", "r")
    KEY = str(key_file.read())
    gmaps = googlemaps.Client(key=KEY)

    geocode = gmaps.geocode(address)
    orig_lat, orig_lng = map_methods.getlatlng(geocode)

    rad_lat, rad_lng = map_methods.dist2deg(radius, orig_lat, orig_lng)

    X = np.linspace(orig_lng-rad_lng, orig_lng+rad_lng, grid)
    Y = np.linspace(orig_lat-rad_lat, orig_lat+rad_lat, grid)

    xx, yy = np.meshgrid(X, Y)

    coordinates = np.array(list(zip(np.ndarray.flatten(xx), np.ndarray.flatten(yy)))) # [0] is lng [1] is lat

    dests = map_methods.coord_format(coordinates[0][1], coordinates[0][0])
    for i in range(1, grid**2):
        dests = dests + '|' + map_methods.coord_format(coordinates[i][1], coordinates[i][0])
    origin = map_methods.coord_format(orig_lat, orig_lng)

    dmatrix = gmaps.distance_matrix(origin, dests, mode=mode)
    times = map_methods.get_times(dmatrix)

    rows = []
    for i in range(grid):
        rows.append(times[0+i*grid:grid+i*grid])
    Z = np.stack(rows)

    return X, Y, Z





def get_map(address, zoom):

def zoom_to_radius(zoom, latitude):
    '''
    Assumes 640x640 image

    :param zoom: google static maps API zoom. int (1-20)
    :param latitude: from equator, degrees
    :return: radius to search based on zoom in km
    '''

    metersPerPx = 156543.03392 * Math.cos(latitude * Math.PI / 180) / Math.pow(2, zoom)

    return metersPerPx / 1000.0 * (MAX_STATIC_MAP_SIZE // 2)

