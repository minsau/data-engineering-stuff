from math import sin, cos, sqrt, atan2, radians
from src.config import settings

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
    home_location_str = settings.HOME_LOCATION
    home = tuple(map(float, home_location_str.split(',')))
    return get_distance_in_km_between_two_points(home, destiny)