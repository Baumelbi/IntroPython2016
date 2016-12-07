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
import gmplot
import requests
import webbrowser
import os
from geopy.geocoders import Nominatim


def manualLocation(geolocator):
	userInput = input("Please enter an address or location in Seattle: ")
	location = geolocator.geocode(userInput)
	while "seattle" not in location.address.lower():
		userInput = input("Please enter an address or location in Seattle: ")
		location = geolocator.geocode(userInput)

	results(location.longitude, location.latitude, location.address)

def ipLocation(geolocator):
	print ("Estimating location based on IP address")
	# This call makes a request to a website that will
	# give a rough estimate of your location based on your public IP adress
	r = requests.get("http://freegeoip.net/json/")
	data = r.json()
	latlong = str(data["latitude"])+","+str(data["longitude"])
	
	#44.9778, -93.2650 hard coded non seattle location to test
	#location = geolocator.reverse("44.9778, -93.2650") 
	location = geolocator.reverse(latlong)

	if "seattle" not in location.address.lower():
		print("You are not located in Seattle")
		manualLocation(geolocator)
	
	else:
		results(location.longitude, location.latitude, location.address)

def results(longitude, latitude, address):
	print()
	radius = float(eval(input("What radius would you like in miles? "))*1609)
	limit = int(eval(input("How many results would you like? (1000 - 50,000) ")))
	goodLimit = False
	
	while (not goodLimit):
		if amount >= 1000 and amount <= 50000:
			goodLimit = True
		else:
			limit = int(eval(input("How many results would you like? (1000 - 50,000) ")))
	
	query = ("https://data.seattle.gov/resource/pu5n-trf4.json?$limit={}&$where=within_circle(incident_location,{},{},{})".format(limit,latitude,longitude,radius))

	raw_data = pd.read_json(query)

	# taking the parsed JSon and alligning it with the map
	gmap = gmplot.GoogleMapPlotter(latitude, longitude, 13)
	gmap.heatmap(raw_data["latitude"], raw_data["longitude"], radius = 30)
	gmap.draw("mymap.html")

	# opens up the html file in your default browser
	url = "mymap.html"
	webbrowser.open('file://' + os.path.realpath(url))
	
	# gives you the text data for the selected area limited to 5000 results
	counts = raw_data['event_clearance_group'].value_counts()
	print()
	print('Crime events by count in your area')
	print(address)
	print()
	print(counts)

def main():
	geolocator = Nominatim()
	go = True

	print("This app will generate a crime heat map based on your location")

	while go:
		intro = input("Would you like to enter a location(y/n): ")
		if intro.lower() == "y":
			go = False
			manualLocation(geolocator)
		elif intro.lower() == "n":
			go = False
			ipLocation(geolocator)
		

if __name__ == '__main__':
   main()
