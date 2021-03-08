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

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
point = organization["geometry"]["coordinates"]
hours = organization['properties']['CompanyMetaData']['Hours']['text']
org_point = "{0},{1}".format(point[0], point[1])
delta = "0.005"
map_params = {
    "spn": ",".join([delta, delta]),
    "l": "map",
    "pt": f"{org_point},pm2dgl~{org_point1},pm2dgl",
}
org = [float(i) for i in org_point.split(',')]
org1 = [float(i) for i in org_point1.split(',')]
a = str(((org1[0] - org[0]) ** 2 + (org1[1] - org[1]) ** 2) ** 0.5 * 111.111)
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
intro_text = [org_name, org_address, hours, f'Расстояние : {a}км']
while pygame.event.wait().type != pygame.QUIT:
    font = pygame.font.Font(None, 25)
    text_coord = 50
    screen.blit(pygame.image.load(map_file), (0, 0))
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()
pygame.quit()
os.remove(map_file)