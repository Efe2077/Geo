import requests


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def geocode(address):
    geocode_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"
    }

    request = requests.get(geocode_api_server, params=geocoder_params)
    json_request = request.json()
    toponyms = json_request['response']['GeoObjectCollection']['featureMember']
    return toponyms[0]['GeoObject'] if toponyms else None


def get_coordinates(address):
    toponym = geocode(address)
    toponym_coord = toponym['Point']['pos']
    toponym_long, toponym_lat = toponym_coord.split()
    return float(toponym_long), float(toponym_lat)


def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)
    toponym_coord = toponym['Point']['pos']
    toponym_long, toponym_lat = toponym_coord.split()
    ll = ','.join([toponym_long, toponym_lat])
    env = toponym['boundedBy']['Envelope']
    l, b = env['lowerCorner'].split(' ')
    r, t = env['upperCorner'].split(' ')
    dx = abs(float(l) - float(r)) / 2
    dy = abs(float(t) - float(b)) / 2
    span = f'{dx},{dy}'
    return ll, span
