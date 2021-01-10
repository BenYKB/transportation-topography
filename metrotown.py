import map_methods
import json
import googlemaps
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt

key_file = open("key.txt", "r")
KEY = str(key_file.read())

GRID = 5
RADIUS = 5.0 # [km]
address = '4700 Kingsway, Burnaby, BC'

gmaps = googlemaps.Client(key=KEY)

# metrotown_geocode = gmaps.geocode('4700 Kingsway, Burnaby, BC')
# with open('metrotown_geocode.txt') as f:
#     metrotown_gc = json.load(f)
# print(metrotown_gc[0]['geometry']['location']['lat'])

f = open('metrotown_geocode.txt','r')
mt_lat, mt_lng = map_methods.getlatlng(f)

rad_lat, rad_lng = map_methods.dist2deg(RADIUS, mt_lat, mt_lng)

X = np.linspace(mt_lng-rad_lng, mt_lng+rad_lng, GRID)
Y = np.linspace(mt_lat-rad_lat, mt_lat+rad_lat, GRID)

xx, yy = np.meshgrid(X, Y)
# plt.plot(xx, yy, marker='.', color='k', linestyle='none')
# plt.show()

coordinates = np.array(list(zip(np.ndarray.flatten(xx), np.ndarray.flatten(yy)))) # [0] is lng [1] is lat

dests = map_methods.coord_format(coordinates[0][1], coordinates[0][0])
for i in range(1, GRID**2):
    dests = dests + '|' + map_methods.coord_format(coordinates[i][1], coordinates[i][0])
origin = map_methods.coord_format(mt_lat, mt_lng)


noon = datetime.now()
noon = noon.replace(hour=12,minute=0,second=0,microsecond=0)
# dmatrix = gmaps.distance_matrix(origin, dests, mode='transit', departure_time=noon)
# with open('metrotown_times_transit.txt', 'w') as f:
#     json.dump(dmatrix ,f)
# print(type(dmatrix)) # dict

f = open('metrotown_times_transit.txt', 'r')
times = map_methods.get_times(f)
print(times)

rows = []
for i in range(GRID):
  rows.append(times[0+i*GRID:GRID+i*GRID])

Z = np.stack(rows)

#data = zip(np.ndarray.flatten(xx), np.ndarray.flatten(yy), times)

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






