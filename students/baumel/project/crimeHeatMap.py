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
	prompt = "Please enter an address or location in Seattle: "
	
	userInput = input(prompt)
	location = geolocator.geocode(userInput)	

	return location

def ipLocation(geolocator):
	print ("Estimating location based on IP address")
	# This call makes a request to a website that will
	# give a rough estimate of your location based on your public IP adress
	# This API occasionally times out, if so you just need to run the program again or manually enter address
	r = requests.get("http://freegeoip.net/json/")
	data = r.json()
	latlong = str(data["latitude"])+","+str(data["longitude"])
	
	#44.9778, -93.2650 hard coded non seattle location to test
	#location = geolocator.reverse("44.9778, -93.2650") 
	
	location = geolocator.reverse(latlong)
	
	return location

def radiusAndLimit():
	goodLimit = False
	goodRadius = False

	while (not goodLimit):
		limit = input("How many results would you like? (1000 - 50,000) ")
		
		try:
			int(limit)
		except ValueError:
			print ("Invalid value entered!")
		else:
			limit = int(limit)
			if limit >= 1000 and limit <= 50000:
				goodLimit = True
			else:
				print ("Invalid amount entered!")

	while (not goodRadius):
		radius = input("What radius would you like in miles? (.1 - 1000.0) ")
		
		try:
			float(radius)
		except ValueError:
			print ("Invalid value entered!")
		else:
			radius = float(radius)
			if radius >= 0.1 and radius <= 1000.0:
				goodRadius = True
				radius = radius * 1609 #conversion to meters for the API call
			else:
				print ("Invalid amount entered!")

	return radius, limit

def validLocation(geolocator, inputOption):


	if inputOption == "n":
		location = ipLocation(geolocator)
	else:
		location = manualLocation(geolocator)

	while location is None or "seattle" not in location.address.lower():
			location = manualLocation(geolocator)
	
	latitude = geolocator.geocode(location).latitude
	longitude = geolocator.geocode(location).longitude
	address = geolocator.geocode(location).address
	radius, limit = radiusAndLimit()

	#Returns a dictionary of location items that will be used throughout the program
	return {'location': location, 
			'radius': radius, 
			'limit':limit, 
			'latitude':latitude, 
			'longitude': longitude,
			'address': address}

	


def apiResults(locationInfo):
	query = ("https://data.seattle.gov/resource/pu5n-trf4.json?$limit={}&$where=within_circle(incident_location,{},{},{})"
		.format(locationInfo['limit'],
				locationInfo['latitude'],
				locationInfo['longitude'],
				locationInfo['radius']))
	return pd.read_json(query)
	
def mapMaker(raw_data, locationInfo):
	# taking the parsed JSon and alligning it with the map
	gmap = gmplot.GoogleMapPlotter(locationInfo['latitude'],locationInfo['longitude'], 13)
	gmap.heatmap(raw_data["latitude"], raw_data["longitude"], radius = 30)
	gmap.draw("mymap.html")


def output(raw_data, locationInfo):
	# opens up the html file in your default browser
	url = "mymap.html"
	webbrowser.open('file://' + os.path.realpath(url))
	
	# gives you the text data for the selected area limited to 5000 results
	counts = raw_data['event_clearance_group'].value_counts()
	print()
	print('Crime events by count in your area')
	print(locationInfo['address'])
	print()
	print(counts)


def main():
	geolocator = Nominatim()
	intro = True
	again = True

	print("This app will generate a crime heat map based on your location")

	while intro:
		introText = input("Would you like to enter a location (y/n) ")
		if introText.lower() == "y" or introText.lower() == "n":
			locationInfo = validLocation(geolocator, introText)
			intro = False
	
	raw_data = apiResults(locationInfo)
	mapMaker(raw_data, locationInfo)
	output(raw_data, locationInfo)
	
	while again:
		againText = input("Would you like to run the application again (y/n) ")
		if againText.lower() == "y" or againText.lower() == "n":
			again = False
		if againText.lower() == "y":
			main()
		else:
			print("Thanks! See you next time")
			SystemExit
		

if __name__ == '__main__':
   main()
