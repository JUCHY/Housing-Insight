# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 02:21:59 2020

@author: joshu
"""

import googlemaps
import math
import apiconfig



#uses google's geocoding api to get Latitude and Longitudes of given address
def getLatLong(address):
    gmaps = googlemaps.Client(key=apiconfig.API['GoogleMapKey'])
    geocode = gmaps.geocode(address)
    lat = geocode[0]['geometry']['location']['lat']
    lng = geocode[0]['geometry']['location']['lng']
    return [ lng, lat]

#uses haversine formula to compute the distance(miles) between two points
def computeDistance(position1, position2):
    R = 3958.8
    long = position1[0]
    lat = position1[1]
    long2 = position2[0]
    lat2 = position2[1]
    rlat1 = lat * (math.pi/180)
    rlat2 = lat2 * (math.pi/180)
    difflat = rlat2-rlat1 #radian difference latitude
    difflong = (long-long2)* (math.pi/180) #radian difference longitude
    d = 2 * R * math.asin(math.sqrt(math.sin(difflat/2)*math.sin(difflat/2)+math.cos(rlat1)*math.cos(rlat2)*math.sin(difflong/2)*math.sin(difflong/2)));
    return d


print(getLatLong('717 Franklin Ave, Brooklyn, NY 11238'))