# http://planetpixelemporium.com/tutorialpages/light.html
import colorsys

kelvin_temperature_colors = {

    "candle": (255, 147, 41),
    "40w_tungsten": (255, 197, 143),
    "100w_tungsten": (255, 214, 170),
    "halogen": (255, 241, 224),
    "carbon_arc": (255, 250, 244),
    "high_noon_sun": (255, 255, 251),
    "direct_sunlight": (255, 255, 255),  # white
    "overcast_sky": (201, 226, 255),
    "clear_blue_sky": (64, 156, 255),
}
background_colors = {
    'black': (0, 0, 0),
    'gray': (127, 127, 127),
    'light_gray': (180, 180, 180),
    'blueberry': (127, 127, 255),
}
strip_colors = {
    # for top edge
    'high_th': (150, 65, 90),
    'mid_th': (65, 55, 90),
    'low_th': (48, 65, 95),
    'purple': (127, 0, 255),
    # for bottom edge
    'high_ca': (137, 64, 109),
    'mid_ca': (120, 75, 55),
    'low_ca': (150, 75, 10),
}


def color_distance(left, right):
    return sum((l - r) ** 2 for l, r in zip(left, right)) ** 0.5


def color_label(color):
    """convert a rgb to a color name"""

    key_colors = {**kelvin_temperature_colors, **background_colors, **strip_colors}
    nearest_color = lambda key_colors: color_distance(color, key_colors[1])

    label, key_color = min(key_colors.items(), key=nearest_color)
    is_backgound_color = label in background_colors or label in kelvin_temperature_colors
    return label, not is_backgound_color


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h,s,v = colorsys.rgb_to_hsv(r, g, b)
    h,s,v = round(h, 6), round(s, 6), round(v, 6)
    return h,s,v
