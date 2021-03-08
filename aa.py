def selection_of_scale(json_response):
    a = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]['boundedBy']['Envelope']
    b = [float(i) for i in a['lowerCorner'].split()]
    c = [float(i) for i in a['upperCorner'].split()]
    x, y = c[0] - b[0], c[1] - b[1]
    return ",".join([str(x), str(y)])