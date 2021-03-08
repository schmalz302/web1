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
org_point1 = ",".join(toponym["Point"]["pos"].split(" "))

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
address_ll = "37.588392,55.734036"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": org_point1,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
json_response = response.json()

points = []
organization = json_response["features"]
for i in range(10):
    point = organization[i]["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    try:
        a = organization[i]['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['TwentyFourHours']
        if a:
            org_point = f"{org_point},pm2gnl"
    except KeyError:
        try:
            a = organization[i]['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['Everyday']
            if a:
                org_point = f"{org_point},pm2bll"
        except KeyError:
            org_point = f"{org_point},pm2grl"
        org_point = f"{org_point},pm2grl"
    points.append(org_point)
points = '~'.join(points)
delta = "0.005"
map_params = {
    "spn": ",".join([delta, delta]),
    "l": "map",
    "pt": points,
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
while pygame.event.wait().type != pygame.QUIT:
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)