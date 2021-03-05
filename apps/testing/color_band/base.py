from collections import OrderedDict


class BaseColorBand:
    # location on pic
    location = (None, None)
    # raw data of color band
    raw_color_band = {}

    @classmethod
    def linear_interpolate(cls, color_band: dict):
        """fill the empty value of color band using interpolation"""

        # color_band = sorted(color_band)
        color_band_list = sorted(color_band.items())

        assert color_band_list[0][1], "the start of color band can't be none"
        assert color_band_list[-1][1], "the end of color band can't be none"

        result_colorband = OrderedDict(color_band)
        previous_value = None
        previous_rgb = None
        for index, item in enumerate(color_band_list):
            value, rgb = item
            if rgb:
                previous_value = value
                previous_rgb = rgb
                continue
            else:
                for i in range(index + 1, len(color_band_list)):
                    next_value, next_rgb = color_band_list[i]
                    if next_rgb:
                        rgb_offset = (next_rgb[0] - previous_rgb[0],
                                      next_rgb[1] - previous_rgb[1],
                                      next_rgb[2] - previous_rgb[2])
                        percent = (value - previous_value) / (next_value - previous_value)
                        result_colorband[value] = (round(previous_rgb[0] + rgb_offset[0] * percent),
                                             round(previous_rgb[1] + rgb_offset[1] * percent),
                                             round(previous_rgb[2] + rgb_offset[2] * percent))
                        continue
        return OrderedDict(result_colorband)

    @classmethod
    def get_colorband(cls, interpolation=False):
        color_band_list = sorted(cls.raw_color_band.items())
        assert color_band_list[0][1], "the start of color band can't be none"
        assert color_band_list[-1][1], "the end of color band can't be none"

        if not interpolation:
            # stand color band, remove all none value
            return OrderedDict([item for item in color_band_list if item[1]])
        else:
            return cls.linear_interpolate(cls.raw_color_band)
