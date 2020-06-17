# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:15:53 2020

@author: joshu
"""

from fastkml import kml
import dataprocessing


    
def findprecinct(p, dat):
    precincts = kml.KML()
    precincts.from_string(dat)
    features = list(precincts.features())
    f2 = list(features[0].features())
    f3 = list(f2[0].features())
    for x in f3:
        placemark = x.geometry
        polygons = list(placemark.geoms)
        finallist = []
        for y in polygons:
            finallist = finallist + list(y.exterior.coords)
        finalpolygon = dataprocessing.getPolygon(finallist)
        if dataprocessing.isInside(finalpolygon, len(finallist)-1, p):
            return x.extended_data.elements[0].value
        
        
def finddistrict(p, dat):
    districts  = kml.KML()
    districts.from_string(dat)
    features = list(districts.features())
    f2 = list(features[0].features())
    f3 = list(f2[0].features())
    for x in f3:
        placemark = x.geometry
        polygons = list(placemark.geoms)
        finallist = []
        for y in polygons:
            finallist = finallist + list(y.exterior.coords)
        finalpolygon = dataprocessing.getPolygon(finallist)
        if dataprocessing.isInside(finalpolygon, len(finallist)-1, p):
            return x.extended_data.elements[0].value
            
