#!/usr/bin/env python
# coding: utf-8

# In[2]:


from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='your_app_name')

addresses = [
            '1175, W Cleveland St, Fayetteville, Arkansas, 72701, United States of America',
]

coordinates = []

for address in addresses:
    location = geolocator.geocode(address)

    lat, lon = location.latitude, location.longitude

    coordinates.append((lat, lon))

print(coordinates)


# In[ ]:




