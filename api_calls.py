import map_methods
import googlemaps
from datetime import datetime
import numpy as np

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





