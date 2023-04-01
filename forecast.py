import requests

template_query = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&hourly=cloudcover,visibility&daily=sunrise,sunset&timeformat=unixtime"
max_cloudcover = 100
max_visibility = 240000

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
				"cloudcover": jres["hourly"]["cloudcover"][i] / max_cloudcover,
				"visibility": jres["hourly"]["visibility"][i] / max_visibility
			})
		daily_data.append({
			"sunrise": jres["daily"]["sunrise"][day],
			"sunset": jres["daily"]["sunset"][day],
			"hourly": hourly_data
		})
	return daily_data

def forecast(lat, long, tz):
	return parse_forecast(req_forecast(lat, long, tz))

# test
# test_data = (36.0663068, -94.1738257, "America/Chicago")
# print(req_forecast(*test_data))
# print(forecast(*test_data))



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
