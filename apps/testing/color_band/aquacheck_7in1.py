from collections import OrderedDict

from apps.testing.color_band.base import BaseColorBand


class PHColorBand(BaseColorBand):
    location = (200, 200)

    raw_color_band = {
        6.2: (207, 141, 10),
        6.5: None,
        6.8: (201, 118, 23),
        7.0: None,
        7.2: (196, 95, 34),
        7.5: None,
        7.8: (190, 75, 43),
        8.1: None,
        8.4: (182, 52, 51),
    }


class CalciumHardnessColorBand(BaseColorBand):
    location = (100, 100)
    raw_color_band = {}


class FreeChlorineColorBand(BaseColorBand):
    location = (100, 100)
    raw_color_band = {}


class TotalChlorineColorBand(BaseColorBand):
    location = (100, 100)
    raw_color_band = {}


class TotalBromineColorBand(BaseColorBand):
    location = (100, 100)
    raw_color_band = {}


class TotalAlkainityColorBand(BaseColorBand):
    location = (100, 100)
    raw_color_band = {}


class CyanuricAcidColorBand(BaseColorBand):
    location = (100, 100)
    raw_color_band = {}
