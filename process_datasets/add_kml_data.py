#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020
@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.sql.functions import lit
import testingprocesses
import polygon
import boto3




sc = SparkContext("local", "SparkFile App")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/testingprocesses.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/polygon.py")

s3 = boto3.resource('s3')
obj1 = s3.Object('living-insight-data', "Police Precincts.kml")
obj2 = s3.Object('living-insight-data', "Community Districts.kml")
precincts = obj1.get()['Body'].read()
districts = obj2.get()['Body'].read()

def process_precincts(row, dat=precincts):
    p = polygon.Point(row.longitude,row.latitude)
    precinct = testingprocesses.findprecinct(p, dat)
    data = row.asDict()
    try:
        data["precinct"] = int(precinct)
    except:
        data["precinct"] = precinct
    return Row(**data)
    
def process_districts(row, dat=districts):
    p = polygon.Point(row.longitude, row.latitude)
    district = testingprocesses.finddistrict(p,dat)
    data = row.asDict()
    try:
        data["community_district"] = int(district)
    except:
        data["community_district"] = district
    return Row(**data)



spark = SparkSession \
    .builder \
    .appName("Process to pSqL") \
    .getOrCreate()
    
    
    
buildings = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","buildings") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()
    

print(buildings.head(5))
building_with_precinct_rdd = buildings.withColumn("precinct", lit(int(1))).rdd.map(process_precincts)
building_with_precinct = building_with_precinct_rdd.toDF()
print(building_with_precinct.head(5))
building_with_districts_rdd = building_with_precinct.withColumn("community_district", lit(int(1))).rdd.map(process_districts)
building_with_districts = building_with_districts_rdd.toDF()
print(building_with_districts.head(5))
building_with_districts.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="buildings_with_kml",properties = { "user" : "postgres", "password" : "postgres" })
    


#air_quality.write.jdbc( )

spark.stop()
