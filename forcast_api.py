import requests, geohash

BOM_EP = 'https://api.cloud.bom.gov.au/forecasts/v1/grid'
TH_TEMP = '/three-hourly/{geohash}/temperatures'
TH_PREC = '/three-hourly/{geohash}/precipitation'
TH_ICON = '/three-hourly/{geohash}/icons'
MIME_TYPE_JSON = 'application/json'
API_KEY = 'pauJiXCOfD2Fty7MhpUtS2qEY3Njm7rV1uy2GGOy'

def connect(url, headers):
    r = requests.get(url, headers=headers)
    print('attempting connection to {}...'.format(url))
    print('response was [{} {}]'.format(r.status_code, r.reason))
    return r

def get_temperature(geohash):
    url = "{}{}".format(BOM_EP, TH_TEMP.replace('{geohash}', geohash))
    headers = {'Accept': MIME_TYPE_JSON, 'x-api-key': API_KEY}
    return connect(url, headers)

def get_precipitation(geohash):
    url = "{}{}".format(BOM_EP, TH_PREC.replace('{geohash}', geohash))
    headers = {'Accept': MIME_TYPE_JSON, 'x-api-key': API_KEY}
    return connect(url, headers)

def get_icon(geohash):
    url = "{}{}".format(BOM_EP, TH_ICON.replace('{geohash}', geohash))
    headers = {'Accept': MIME_TYPE_JSON, 'x-api-key': API_KEY}
    return connect(url, headers)

def get_geohash(lat, lon):
    return geohash.encode(lat, lon, precision=7)

if __name__ == '__main__':
    g = get_geohash(-35.332056, 149.125750)
    r = get_icon(g)
    j = r.json()
    print(j)
