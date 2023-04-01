import math
import random
import requests

template_query = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&hourly=cloudcover,visibility&daily=sunrise,sunset"
MAX_CLOUDCOVER = 100
MAX_VISIBILITY = 240000
# MAX_DIFFUSE_RADIATION = 1000

def req_forecast(latitude, longitude, timezone):
	return requests.get(template_query.format(latitude=latitude, longitude=longitude, timezone=timezone)).json()

def parse_forecast(jres):
	daily_data = []
	for day in range(0, len(jres["daily"]["time"])):
		hourly_data = []
		for hour in range(0, 24):
			i = 24 * day + hour
			hourly_data.append({
				"time": jres["hourly"]["time"][i],
				"cloudcover": jres["hourly"]["cloudcover"][i] / MAX_CLOUDCOVER,
				"visibility": jres["hourly"]["visibility"][i] / MAX_VISIBILITY
			})
		daily_data.append({
			"sunrise": jres["daily"]["sunrise"][day],
			"sunset": jres["daily"]["sunset"][day],
			"hourly": hourly_data
		})
	return daily_data

def forecast(lat, long, tz):
	return parse_forecast(req_forecast(lat, long, tz))


# num days is 3
internal_template_query = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&hourly=cloudcover,visibility&daily=sunrise,sunset&forecast_days=3&timeformat=unixtime"

# dt is 1 minute
def internal_forecast(latitude, longitude, timezone):
	res = requests.get(internal_template_query.format(latitude=latitude, longitude=longitude, timezone=timezone)).json()
	#return res
	data = []
	for hour in range(0, len(res["hourly"]["time"])):
		hour_info = res["hourly"]
		# not the most accurate but time crunch
		cloudcover = (1 - (hour_info["cloudcover"][hour] / MAX_CLOUDCOVER))
		visibility = (hour_info["visibility"][hour] / MAX_VISIBILITY)
		y = cloudcover * visibility
		for minute in range(0, 60):
			time = hour_info["time"][hour] + minute
			day_night = 1 if (res["daily"]["sunrise"][math.floor(hour / 24)] <= time and time <= res["daily"]["sunset"][math.floor(hour / 24)]) else 0
			y *= day_night
			data.append(max(0, min(6 * (y + random.random() / 100), 1)))
	return data


# test
test_data = (36.0663068, -94.1738257, "America/Chicago")
# print(req_forecast(*test_data))
# print(forecast(*test_data))
print(internal_forecast(*test_data))




# import requests
# from datetime import datetime
# from dateutil import tz
#
# #query = r"""https://api.open-meteo.com/v1/forecast?latitude=36.06&longitude=-94.16&hourly=cloudcover,visibility&daily=sunrise,sunset&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=3&timezone=America%2FChicago"""
#
# def convert_time(iso_time_str):
# 	central = tz.gettz('America/Chicago')
# 	return datetime.fromisoformat(iso_time_str).astimezone(central)
#
# print(convert_time("2023-03-31T07:02"))
# exit()
#
# def get_forecast():
# 	data = requests.get(query).json()
#
# 	H_R, D_R = data['hourly'], data['daily']
# 	H_data = list(zip(H_R['time'], H_R['cloudcover']))
# 	D_data = list(zip(D_R['sunrise'], D_R['sunset']))
#
# 	print(H_data)
# 	print(D_data)
#
# if __name__ == "__main__":
#	print(get_forecast())
