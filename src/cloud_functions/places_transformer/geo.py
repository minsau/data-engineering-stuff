import arrow
from math import sin, cos, sqrt, atan2, radians
from .config import get_app_secrets
import googlemaps

secrets = get_app_secrets()
gmaps = googlemaps.Client(key=secrets.GOOGLE_MAPS_API_KEY)

# Approximate radius of earth in km
R = 6373.0

def get_distance_in_km_between_two_points(origin: tuple, destiny: tuple) -> float:
    origin_lat = radians(origin[0])
    origin_lng = radians(origin[1])
    destiny_lat = radians(destiny[0])
    destiny_lng = radians(destiny[1])

    dlon = destiny_lng - origin_lng
    dlat = destiny_lat - origin_lat

    a = sin(dlat / 2)**2 + cos(origin_lat) * cos(destiny_lat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_distance_from_home_in_km(destiny: tuple) -> float:
    home_location_str = secrets.HOME_LOCATION
    home = tuple(map(float, home_location_str.split(',')))
    return get_distance_in_km_between_two_points(home, destiny)

def get_geocode_by_place_name(place_name, visited) -> dict:
    geocode_result = gmaps.geocode(place_name)
    if len(geocode_result) == 0:
        print(f'No results found for {place_name}')
        return {}
    datetime = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    gdict = {
        'place_name_list': place_name,
        'formatted_address': geocode_result[0]['formatted_address'],
        'location': f'{latitude},{longitude}',
        'place_id': geocode_result[0]['place_id'],
        'visited': visited,
        'distance_from_home_in_km': get_distance_from_home_in_km((latitude, longitude)),
        'datetime': datetime
    }
    return gdict