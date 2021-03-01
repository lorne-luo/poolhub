import colour
from django.utils.module_loading import import_string

DEFAULT_STRIP_NAME = 'aquacheck_7in1'


def get_strip_metadata(strip_name):
    return import_string(f'apps.testing.color_band.{strip_name}')


def get_color_band(strip, chemistry):
    return getattr(strip, f'{chemistry.value}_COLOR_BAND')


def pick_color(image, chemistry_name, strip):
    location = getattr(strip, f'{chemistry_name.value}_LOCATION')
    return image.getpixel(location)


def color_distance(rgb1, rgb2):
    rd = (rgb1[0] - rgb2[0]) ** 2
    gd = (rgb1[1] - rgb2[1]) ** 2
    bd = (rgb1[2] - rgb2[2]) ** 2
    return (rd + gd + bd) ** 0.5


def calculate_distances(color, color_band):
    distances = {}
    for value, rgb in color_band.items():
        distances[value] = colour.delta_E(rgb, color)

    return distances


def cal_linear_value(color_band, distances):
    """calculate linear value from color band"""
    min_value = min(distances, key=distances.get)
    max_value = max(distances, key=distances.get)
    closest_values = sorted(distances, key=distances.get)
    cloest_color1 = color_band[closest_values[0]]
    distance1 = distances[closest_values[0]]
    cloest_color2 = color_band[closest_values[1]]
    distance2 = distances[closest_values[1]]

    direct_distance = colour.delta_E(cloest_color1, cloest_color2)
    print(distance1, distance2, direct_distance)
    return distance1, distance2, direct_distance


def read_chemistry(image, chemistry, strip_name=DEFAULT_STRIP_NAME, return_linear=True):
    strip = get_strip_metadata(strip_name)
    color_band = get_color_band(strip, chemistry)
    color = pick_color(image, chemistry, strip)

    distances = calculate_distances(color, color_band)
    if not return_linear:
        return min(distances, key=distances.get)
    else:
        return cal_linear_value(color_band, distances)
