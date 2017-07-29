from geopy.geocoders import Nominatim

def geocode(name):
    geolocator = Nominatim()
    location = geolocator.geocode(name)
    print('raw:', location.raw)
    print('coords:', (location.latitude, location.longitude))
    return location
    
def reverse(lat, lon):
    geolocator = Nominatim()
    location = geolocator.geocode('{}, {}'.format(lat, lon))
    print('raw:', location.raw)
    print('address:', location.address)
    return location

if __name__ == '__main__':
    geocode('175 5th Avenue NYC')
    reverse('52.509669', '13.376294')