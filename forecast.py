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


internal_template_query = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&hourly=cloudcover,visibility,direct_radiation,diffuse_radiation&forecast_days=3"

def internal_forecast(latitude, longitude, timezone):
	res = requests.get(internal_template_query.format(latitude=latitude, longitude=longitude, timezone=timezone)).json()
	data = []
	for i in range(0, len(res["hourly"]["time"])):
		x = res["hourly"]
		# not the most accurate but whatever
		cloudcover = (1 - (x["cloudcover"][i] / MAX_CLOUDCOVER))
		visibility = (x["visibility"][i] / MAX_VISIBILITY)
		radiation = (x["diffuse_radiation"][i] / (1 + x["diffuse_radiation"][i] + x["direct_radiation"][i]))
		y = cloudcover * visibility * radiation
		for l in range(0, 60):
			data.append(max(0, min(y + random.random() / 100, 1)))
	return data


if __name__ == "__main__":
	test_data = (36.0663068, -94.1738257, "America/Chicago")
	# print(req_forecast(*test_data))
	# print(forecast(*test_data))
	print(internal_forecast(*test_data))