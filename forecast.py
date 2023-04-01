import requests
from datetime import datetime
from dateutil import tz

query = r"""https://api.open-meteo.com/v1/forecast?latitude=36.06&longitude=-94.16&hourly=cloudcover,visibility&daily=sunrise,sunset&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=3&timezone=America%2FChicago"""

def convert_time(iso_time_str):
    central = tz.gettz('America/Chicago')
    return datetime.fromisoformat(iso_time_str).astimezone(central)

print(convert_time("2023-03-31T07:02"))
exit()

def get_forecast():
    data = requests.get(query).json()
    
    H_R, D_R = data['hourly'], data['daily']
    H_data = list(zip(H_R['time'], H_R['cloudcover']))
    D_data = list(zip(D_R['sunrise'], D_R['sunset']))

    print(H_data)
    print(D_data)
if __name__ == "__main__":
    print(get_forecast())