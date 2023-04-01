from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='helios')

def getCoords(address):
	location = geolocator.geocode(address)
	return (location.latitude, location.longitude)

# test
address = '1175, W Cleveland St, Fayetteville, Arkansas, 72701, United States of America'
print(getCoords(address))
