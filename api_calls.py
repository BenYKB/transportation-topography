import map_methods
import googlemaps
from datetime import datetime
import numpy as np
import math

MAX_STATIC_MAP_SIZE = 640
DEFAULT_ZOOM = 15

key_file = open("key.txt", "r")
KEY = str(key_file.read())
gmaps = googlemaps.Client(key=KEY)

def origin_coordinates(address):
    '''
    By google api.

    :param address: human readable address
    :return: lat, lng
    '''
    geocode = gmaps.geocode(address)
    return map_methods.getlatlng(geocode)


def data(address, radius, mode, grid=10):
    ''' Gets x, y and z data related to travel times to locations 
    in specified radius from a specified location.

    :param address: Example: '4700 Kingsway, Burnaby, BC'
                    string. Street address, city, province and/or country. 

    :param radius: float, in km. The radius from the address to map.

    :param mode: "driving", "walking", "bicycling", or "transit"

    :param grid: Spacing of grid. Default is 10
    :type grid: int

    :rtype: X, Y, Z. If N = grid value,
            X: N length array of longitude values
            Y: N length array of latitude values
            Z: NxN array of travel times
    '''
    orig_lat, orig_lng = origin_coordinates(address)

    rad_lat, rad_lng = map_methods.dist2deg(radius, orig_lat, orig_lng)

    X = np.linspace(orig_lng-rad_lng, orig_lng+rad_lng, grid)
    Y = np.linspace(orig_lat-rad_lat, orig_lat+rad_lat, grid)

    xx, yy = np.meshgrid(X, Y)

    coordinates = np.array(list(zip(np.ndarray.flatten(xx), np.ndarray.flatten(yy)))) # [0] is lng [1] is lat
    
    origin = map_methods.coord_format(orig_lat, orig_lng)
    
    N = grid**2
    n = N//25
    r = N%25
    dest_list = []
    for i in range(n):
        dests = map_methods.coord_format(coordinates[0+i*25][1], coordinates[0+i*25][0])
        for i in range(1+i*25, 25+i*25):
            dests = dests + '|' + map_methods.coord_format(coordinates[i][1], coordinates[i][0])
        dest_list.append(dests)
    if r != 0:
        dests = map_methods.coord_format(coordinates[n*25][1], coordinates[n*25][0])
        for i in range(1+n*25, N):
            dests = dests + '|' + map_methods.coord_format(coordinates[i][1], coordinates[i][0])
        dest_list.append(dests)

    if mode != 'transit':
        dmatrix_list = []
        for dests in dest_list:
            dmatrix_list.append(gmaps.distance_matrix(origin, dests, mode=mode))
    else:
        noon = datetime.now()
        noon = noon.replace(hour=12,minute=0,second=0,microsecond=0)
        dmatrix_list = []
        for dests in dest_list:
            dmatrix_list.append(gmaps.distance_matrix(origin, dests, mode='transit', departure_time=noon))
    
    times_list = []
    for dmatrix in dmatrix_list:
        times_list.append(map_methods.get_times(dmatrix))
    times = np.concatenate(times_list)

    Z = np.reshape(times,(grid,grid))

    return X, Y, Z


def get_map_iterator(address, zoom):
    orig_lat, orig_lng = origin_coordinates(address)

    return gmaps.static_map(size=(640,640), center=address, zoom=zoom, style='satellite')


def zoom_to_radius(zoom, latitude):
    '''
    Assumes 640x640 image

#     :param zoom: google static maps API zoom. int (1-20)
#     :param latitude: from equator, degrees
#     :return: radius to search based on zoom in km
#     '''

#     metersPerPx = 156543.03392 * math.cos(latitude * math.PI / 180) / math.pow(2, zoom)

#     return metersPerPx / 1000.0 * (MAX_STATIC_MAP_SIZE // 2)

