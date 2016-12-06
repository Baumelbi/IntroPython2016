"""This program will call to the seattle 911 api and recieve information realting to 
the given latitude and longitude as well as the radius of the circle. The returned
information will be ranked by most common instance to least common

This app will then grab the users current location and use the gmplot library to generate
a heat map of the crime data the user will also have the option to enter in a location
within seattle"""

#!/usr/bin/env python

# before running this app you will need to install:
# numpy
# pandas
# gmplot
# geopy
# you can do this using pip install

import numpy as np
import pandas as pd
#import datetime
#import urllib
import gmplot
#import socket
#from bokeh.plotting import *
#from bokeh.models import HoverTool
#from collections import OrderedDict
import requests
import webbrowser
import os
from geopy.geocoders import Nominatim

geolocator = Nominatim()
go = True
print("This app will generate a crime heat map based on your location")

while go:
	intro = input("Would you like to enter a location(y/n): ")
	if intro.lower() == "y":
		go = False
	elif intro.lower() == "n":
		go = False
if intro.lower() == "y":
	location = input("Please enter an address or location in Seattle: ")
	geo = geolocator.geocode(location)
	
	while "seattle" not in geo.address.lower():
		location = input("Please enter an address or location in Seattle: ")
		geo = geolocator.geocode(location)
	longitude = geo.longitude
	latitude = geo.latitude
	address = geo.address
if intro.lower() == "n":
	print ("Estimating location based on IP address")
	r = requests.get("http://freegeoip.net/json/")
	data = r.json()
	latlong = str(data["latitude"])+","+str(data["longitude"])
	
	# 44.9778, -93.2650 hard coded non seattle location to test
	#location = geolocator.reverse("44.9778, -93.2650") 
	location = geolocator.reverse(latlong)
	
	while "seattle" not in location.address.lower():
		print("You are not currently located in Seattle, please enter a location manually")
		geo = input("Please enter an address or location in Seattle: ")
		location = geolocator.geocode(geo)
	longitude = location.longitude
	latitude = location.latitude
	address = location.address

radius = float(eval(input("what radius would you like in miles: "))*1609)



query = ("https://data.seattle.gov/resource/pu5n-trf4.json?$limit=5000&$where=within_circle(incident_location,{},{},{})".format(latitude,longitude,radius))
raw_data = pd.read_json(query)

# taking the parsed JSon and alligning it with the map
gmap = gmplot.GoogleMapPlotter(latitude, longitude, 13)
gmap.heatmap(raw_data["latitude"], raw_data["longitude"],radius = 20)
gmap.draw("mymap.html")

# opens up the html file in your default browser
url = "mymap.html"
webbrowser.open('file://' + os.path.realpath(url))
counts = raw_data['event_clearance_group'].value_counts()
print('Crime events by count in your area')
print(address)
print()
print(counts)

