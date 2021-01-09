import googlemaps
from datetime import datetime
import json

key_file = open("key.txt", "r")
KEY = str(key_file.read())

gmaps = googlemaps.Client(key=KEY)

def getlat(geocode):
    gc = json.load(geocode)
    return gc[0]['geometry']['location']['lat']

def getlong(geocode):
    gc = json.load(geocode)
    return gc[0]['geometry']['location']['lng']
# metrotown_geocode = gmaps.geocode('4700 Kingsway, Burnaby, BC')
# with open('metrotown_geocode.txt') as f:
#     metrotown_gc = json.load(f)
# print(metrotown_gc[0]['geometry']['location']['lat'])

f = open('metrotown_geocode.txt','r')
print(getlong(f))
