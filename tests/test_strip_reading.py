import os
from unittest.mock import patch

from PIL import Image

from apps.testing.color_band import aquacheck_7in1
from apps.testing.color_band.aquacheck_7in1 import PH_COLOR_BAND
from apps.testing.strip_reading import get_strip_metadata, calculate_distances, get_color_band, read_chemistry, \
    cal_linear_value
from core.constants import Chemistry

TEST_COLOR = (196, 95, 34)


def test_chemistry_read():
    strip = get_strip_metadata('aquacheck_7in1')
    color_band = get_color_band(strip, Chemistry.PH)

    color = TEST_COLOR
    distances = calculate_distances(color, color_band)

    distance1, distance2, direct_distance = cal_linear_value(color_band, distances)
    assert distance1 < distance2

    color = PH_COLOR_BAND[6.8]
    distances = calculate_distances(color, color_band)
    assert distances[6.8] == 0


@patch('apps.testing.strip_reading.pick_color', return_value=PH_COLOR_BAND[6.8])
def test_read_chemistry(mock_pick_color):
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, '..', 'apps/testing/color_band/aquacheck_7in1.jpg')
    image = Image.open(image_path)

    ph_value = read_chemistry(image, Chemistry.PH, return_linear=False)
    assert ph_value == 6.8
