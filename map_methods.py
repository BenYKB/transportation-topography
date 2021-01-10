import json
import numpy as np

LATCONV = 110.574 # [km]
LNGCONV = 111.320 # *cos(latitude) [km]

def getlatlng(geocode):
    gc = json.load(geocode)
    lat = gc[0]['geometry']['location']['lat']
    lng = gc[0]['geometry']['location']['lng']
    return lat, lng

def get_times(dmatrix):
    dmat = json.load(dmatrix)
    length = len(dmat['rows'][0]['elements'])
    times = np.zeros(length)
    # dists = np.zeros(length) 
    for i in range(length):
        times[i] = dmat['rows'][0]['elements'][i]['duration']['value'] # units in ms
    #     dists[i] = dmat['rows'][0]['elements'][i]['distance']['value'] # units in m
    # return times, dists
    return times

def dist2deg(dist, lat, lng):
    lat_deg = dist/LATCONV
    lng_deg = dist/(LNGCONV*np.cos(lat))
    return lat_deg, lng_deg

def coord_format(lat, lng, space=False):
    cma = ','
    if space:
        cma = ', '
    return str(lat) + cma + str(lng)

def printcoord(lat, lng):
    coord = coord_format(lat,lng, space=True)
    print(coord)

def print_pretty(json_dict):
    print(json.dumps(json_dict, indent = 4))