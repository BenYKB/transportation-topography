import googlemaps
from datetime import datetime
import json
import numpy as np
from matplotlib import pyplot as plt

RADIUS = 5.0 # [km]
GRID = 5
LATCONV = 110.574 # [km]
LNGCONV = 111.320 # *cos(latitude) [km]

key_file = open("key.txt", "r")
KEY = str(key_file.read())

gmaps = googlemaps.Client(key=KEY)

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

# metrotown_geocode = gmaps.geocode('4700 Kingsway, Burnaby, BC')
# with open('metrotown_geocode.txt') as f:
#     metrotown_gc = json.load(f)
# print(metrotown_gc[0]['geometry']['location']['lat'])

f = open('metrotown_geocode.txt','r')
mt_lat, mt_lng = getlatlng(f)

rad_lat, rad_lng = dist2deg(RADIUS, mt_lat, mt_lng)

X = np.linspace(mt_lng-rad_lng, mt_lng+rad_lng, GRID)
Y = np.linspace(mt_lat-rad_lat, mt_lat+rad_lat, GRID)

xx, yy = np.meshgrid(X, Y)
# plt.plot(xx, yy, marker='.', color='k', linestyle='none')
# plt.show()

coordinates = np.array(list(zip(np.ndarray.flatten(xx), np.ndarray.flatten(yy)))) # [0] is lng [1] is lat

dests = coord_format(coordinates[0][1], coordinates[0][0])
for i in range(1, GRID**2):
    dests = dests + '|' + coord_format(coordinates[i][1], coordinates[i][0])
origin = coord_format(mt_lat, mt_lng)

# dmatrix = gmaps.distance_matrix(origin, dests, mode='walking')
# with open('metrotown_times.txt', 'w') as f:
#     json.dump(dmatrix ,f)
f = open('metrotown_times.txt', 'r')
times = get_times(f)
# print(times)

rows = []
for i in range(GRID):
  rows.append(times[0+i*GRID:GRID+i*GRID])

Z = np.stack(rows)

data = zip(np.ndarray.flatten(xx), np.ndarray.flatten(yy), times)


# nw_lat = mt_lat + rad_lat
# nw_lng = mt_lng - rad_lng 
# se_lat = mt_lat - rad_lat
# se_lng = mt_lng + rad_lng 
# # printcoord(nw_lat,nw_lng)

# origin = coord_format(mt_lat, mt_lng)
# dests = coord_format(nw_lat, nw_lng) + '|' + coord_format(se_lat,se_lng)

# # dmatrix = gmaps.distance_matrix(origin, dests, mode='walking')
# f = open('metrotown_dists.txt', 'r')
# # dmatrix_dict = json.load(f)
# times = get_times(f)






