import csv
import json
import os
from csv import reader
from datetime import datetime

import cv2

from apps.color_band_training.colors import rgb_to_hsv
from apps.testing.image_process.pre_process import pick_average_color2, white_balance2

""" locate strip from via's json annotation, return the colors picked up """


annotation_json = '/Users/lorneluo/lorne/poolhub/dataset/train/test_strip_anotate_json.json'
image_folder = '/Users/lorneluo/lorne/poolhub/dataset/train/'


def load_strip_annotation(debug=False):
    time_stamp = f"{datetime.now().strftime('%y%m%d-%H%M%S')}"
    debug_folder = f'/Users/lorneluo/lorne/poolhub/dataset/debug/{time_stamp}'
    if not os.path.isdir(debug_folder):
        os.mkdir(debug_folder)

    # 1. read annotation json
    with open(annotation_json) as file:
        strip_json = json.load(file)

    colors_result = {}
    # 2. loop each image, crop and pick colors
    for key, annotation in strip_json.items():
        filename = annotation['filename']
        filepath = os.path.join(image_folder, filename)
        rect = annotation['regions'][0]['shape_attributes']
        x = rect['x']
        y = rect['y']
        width = rect['width']
        height = rect['height']

        img = cv2.imread(filepath)
        crop_img = img[y:y + height, x:x + width]

        # 2.1 calculate color points
        color_points, wb_xy = get_color_points(width, height)
        # print(color_points, wb_xy)

        # 2.2 white balanced
        crop_img, balanced_white = white_balance2(crop_img, wb_xy)

        colors = []
        # 2.3 pick colors
        for x, y in color_points:
            color = pick_average_color2(crop_img, (x, y))
            colors.append(color)

        # 2.4 output debug image
        draw_debug_image(color_points, crop_img, debug_folder, filename, wb_xy)

        colors_result[filename] = colors
        print(filename, colors, balanced_white)

    # 3.write all colors result into csv
    write_color_csv(colors_result, debug_folder)

    rgb_csv_path = os.path.join(debug_folder, 'rgb.csv')
    hsv_csv_path = os.path.join(debug_folder, 'hsv.csv')
    print(f'Write to {rgb_csv_path}')
    print(f'Write to {hsv_csv_path}')


def write_color_csv(colors_result, debug_folder):
    rgb_csv_path = os.path.join(debug_folder, 'rgb.csv')
    with open(rgb_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write header
        writer.writerow(['filename',
                         'th_color_r', 'th_color_g', 'th_color_b', 'th_value',
                         'tc_color_r', 'tc_color_g', 'tc_color_b', 'tc_value',
                         'fc_color_r', 'fc_color_g', 'fc_color_b', 'fc_value',
                         'ph_color_r', 'ph_color_g', 'ph_color_b', 'ph_value',
                         'ta_color_r', 'ta_color_g', 'ta_color_b', 'ta_value',
                         'ca_color_r', 'ca_color_g', 'ca_color_b', 'ca_value'])

        # write colors
        for filename, colors in colors_result.items():
            writer.writerow(
                [filename,
                 *colors[0], '', *colors[1], '', *colors[2], '', *colors[3], '', *colors[4], '', *colors[5], '']
            )

    hsv_csv_path = os.path.join(debug_folder, 'hsv.csv')
    with open(hsv_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write header
        writer.writerow(['filename',
                         'th_color_h', 'th_color_s', 'th_color_v', 'th_value',
                         'tc_color_h', 'tc_color_s', 'tc_color_v', 'tc_value',
                         'fc_color_h', 'fc_color_s', 'fc_color_v', 'fc_value',
                         'ph_color_h', 'ph_color_s', 'ph_color_v', 'ph_value',
                         'ta_color_h', 'ta_color_s', 'ta_color_v', 'ta_value',
                         'ca_color_h', 'ca_color_s', 'ca_color_v', 'ca_value'])

        # write colors
        for filename, colors in colors_result.items():
            hsv_colors=[rgb_to_hsv(*c) for c in colors]
            writer.writerow(
                [filename,
                 *hsv_colors[0], '', *hsv_colors[1], '', *hsv_colors[2], '', *hsv_colors[3], '', *hsv_colors[4], '', *hsv_colors[5], '']
            )
    return rgb_csv_path, hsv_csv_path


def draw_debug_image(color_points, crop_img, debug_folder, filename, wb_xy):
    # draw marker for wb point
    cv2.drawMarker(crop_img, wb_xy, color=(0, 255, 0), markerType=cv2.MARKER_DIAMOND,
                   markerSize=32, thickness=2)
    # draw marker for 7 reading colors
    for x, y in color_points:
        # color = pick_average_color2(debug_img, (x, y))
        cv2.drawMarker(crop_img, (x, y), color=(0, 255, 0), markerType=cv2.MARKER_CROSS,
                       markerSize=32, thickness=2)

    debug_path = os.path.join(debug_folder, filename)
    cv2.imwrite(debug_path, crop_img)


def get_color_points(width, height):
    middle_x = int(width / 2)

    y_factors = [0.04183813443072702,
                 0.2199917695473251,
                 0.4051769547325103,
                 0.5899903978052127,
                 0.7782908093278463,
                 0.9574759945130316]

    y_list = [int(height * i) for i in y_factors]
    color_points = [(middle_x, y) for y in y_list]

    # white balance point
    wb_xy = (middle_x, int(height / 2))
    return color_points, wb_xy



if __name__ == '__main__':
    # from apps.color_band_training import strip_annotation
    # reload(strip_annotation)
    # strip_annotation.load_strip_annotation(True)
    pass
