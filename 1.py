import sys
import pygame
import os
from io import BytesIO
from aa import selection_of_scale
import requests
from PIL import Image

zapros = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": zapros,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()
# данные исходного адреса
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
org_point1 = toponym["Point"]["pos"].split(" ")
delta = "0.005"
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
              "geocode": ','.join(org_point1),
              "format": "json"}

a = requests.get(geocoder_api_server, params=map_params)
a = a.json()
b = []
a = a["response"]["GeoObjectCollection"]["featureMember"]
for i in a:
    c = i["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]
    for j in c:
        if j['kind'] == 'district':
            b.append(j['name'])
if b:
    print(b[0])