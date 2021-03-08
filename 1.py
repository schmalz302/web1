import sys
from io import BytesIO
from aa import selection_of_scale
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

# Преобразуем ответ в json-объект
json_response = response.json()


toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# получаем  координаты  объекта
toponym_coodrinates = toponym["Point"]["pos"]
x1, y1 = toponym_coodrinates.split(" ")
org_point = ",".join([x1, y1])

map_params = {
    "ll": org_point,
    "spn": selection_of_scale(json_response),
    "l": "map",
    "pt": f"{org_point},pm2dgl"
  }
map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
