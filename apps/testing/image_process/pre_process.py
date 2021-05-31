import os
import csv
from collections import OrderedDict

import cv2
import numpy as np
from PIL import Image, ImageEnhance
from tqdm.notebook import tqdm
import pandas as pd
import matplotlib.pyplot as plt

kelvin_table = {
    1000: (255, 56, 0),
    1500: (255, 109, 0),
    2000: (255, 137, 18),
    2500: (255, 161, 72),
    3000: (255, 180, 107),
    3500: (255, 196, 137),
    4000: (255, 209, 163),
    4500: (255, 219, 186),
    5000: (255, 228, 206),
    5500: (255, 236, 224),
    6000: (255, 243, 239),
    6500: (255, 249, 253),
    7000: (245, 243, 255),
    7500: (235, 238, 255),
    8000: (227, 233, 255),
    8500: (220, 229, 255),
    9000: (214, 225, 255),
    9500: (208, 222, 255),
    10000: (204, 219, 255)}

base_folder = '/Users/lorneluo/lorne/poolhub/'
debug_folder = '/Users/lorneluo/lorne/poolhub/dataset/debug'


def calc_color(img_arr):
    """exclude too high or too low point"""
    width, height, _ = img_arr.shape
    sum_color = []
    for x in range(width):
        for y in range(height):
            color = img_arr[x][y]
            sum_color.append((sum(color), color))

    sum_color = sorted(sum_color, key=lambda x: x[0])
    length = len(sum_color)
    middle_colors = sum_color[int(length * 0.35):int(length * 0.45)]
    middle_colors = [c[1] for c in middle_colors]

    b = np.mean([c[0] for c in middle_colors])
    g = np.mean([c[1] for c in middle_colors])
    r = np.mean([c[2] for c in middle_colors])
    return (int(r), int(g), int(b))


def pick_average_color(image, target_pos, sample_size=(32, 32)):
    """pick mean color at given point, for PIL.iImage"""
    if isinstance(image, str):
        image = Image.open(image)

    data = np.asarray(image)

    sub = data[target_pos[0]:target_pos[0] + sample_size[0], target_pos[1]:target_pos[1] + sample_size[1]]
    target_rgb = [np.mean(sub[:, :, i]) for i in range(3)]
    target_color = tuple(map(round, target_rgb))  # RGB float to int
    return target_color


def pick_average_color2(img_arr, target_pos, sample_size=(32, 32), average=True):
    """pick mean color at given point, for cv2"""
    data = cv2.imread(img_arr) if isinstance(img_arr, str) else img_arr
    half_size = int(sample_size[0] / 2)

    if average:
        sub = data[target_pos[1] - half_size:target_pos[1] + half_size,
              target_pos[0] - half_size:target_pos[0] + half_size]
        color = calc_color(sub)
    else:
        color = data[target_pos[1], target_pos[0]]

    return color


def crop_area(image, target_pos, size=(64, 64)):
    if isinstance(image, str):
        image = Image.open(image)

    data = np.asarray(image)
    sub = data[target_pos[0]:target_pos[0] + size[0], target_pos[1]:target_pos[1] + size[1]]
    return Image.fromarray(sub)


def white_balance(image, target_pos, save_path=None):
    """calculate white balance according to WB point, for PIL.Image"""
    if isinstance(image, str):
        image = Image.open(image)

    data = np.asarray(image)
    # sample_size = (16, 16)  # reference sample size
    # sub = data[target_pos[0]:target_pos[0] + sample_size[0], target_pos[1]:target_pos[1] + sample_size[1]]
    # target_color = [np.mean(sub[:, :, i]) for i in range(3)]
    # print(target_color)
    target_color = pick_average_color(image, target_pos, (16, 16))
    # print(1, target_color, max(target_color))

    # calculate white balance
    wb = data.astype(float)
    for i in range(3):
        factor = target_color[i] / float(max(target_color))
        # print(f'Factor={factor}, {type(wb)}')
        wb[:, :, i] /= factor
    wb_image = Image.fromarray(wb.astype(np.uint8))

    target_color = pick_average_color(wb_image, target_pos, (16, 16))
    # print(2, target_color)

    # brightness
    enhancer = ImageEnhance.Brightness(wb_image)
    factor = 200 / target_color[0]  # brightens the image
    result_image = enhancer.enhance(factor)

    target_color = pick_average_color(result_image, target_pos, (16, 16))
    if save_path:
        result_image.save(save_path)

    # print(3, target_color)
    return result_image, target_color


def white_balance2(image, target_pos, save_path=None):
    """calculate white balance according to WB point, for opencv"""
    if isinstance(image, str):
        data = cv2.imread(image)
    else:
        data = image

    target_color = pick_average_color2(data, target_pos, (16, 16))
    # print(1, target_color, max(target_color))

    # calculate white balance
    wb_img = data.astype(float)
    max_channel = max(target_color)
    bright_factor = 200 / max_channel
    for i in range(3):
        factor = target_color[2 - i] / float(max(target_color)) / bright_factor
        # print(f'Factor={factor}')
        wb_img[:, :, i] /= factor

    # target_color = pick_average_color2(wb, target_pos, (16, 16))
    # print(2, target_color)
    if save_path:
        cv2.imwrite(save_path, wb_img)
    # print(3, target_color)
    return wb_img, target_color


def export_white_balance(csv_path):
    input_folder = '/Users/lorneluo/lorne/poolhub/dataset/train'
    output_folder = '/Users/lorneluo/lorne/poolhub/dataset/white_balanced'
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            img_path = os.path.join(input_folder, row[0])
            wb_pos = (int(row[2]), int(row[1]))
            save_path = os.path.join(output_folder, row[0])
            _, balanced_color = white_balance(img_path, wb_pos, save_path)
            # print(row[0], balanced_color)


def process_stripe_image(csv_file):
    """read color from image and save to csv"""
    csv_base_folder = '/Users/lorneluo/lorne/poolhub/dataset/train'
    df = pd.read_csv(csv_file, dtype={'file_path': str,
                                      'white_balance_y': int,
                                      'white_balance_x': int,
                                      'color_y': int,
                                      'color_x': int,
                                      'actual_value': np.number})
    df = df.sort_values('actual_value')

    for i in tqdm(df.index):
        wb_pos = (df.xs(i)['white_balance_x'], df.xs(i)['white_balance_y'])
        color_pos = (df.xs(i)['color_x'], df.xs(i)['color_y'])

        value = df.xs(i)['actual_value']
        file_path = df.xs(i)['file_path']
        path = os.path.join(csv_base_folder, file_path)

        # pick color from image and save to csv
        image = Image.open(path)
        white_balanced_image, wb_color = white_balance(image, wb_pos)
        value_color = pick_average_color(white_balanced_image, color_pos, (16, 16))
        df.at[i, 'value_color_r'] = value_color[0]
        df.at[i, 'value_color_g'] = value_color[1]
        df.at[i, 'value_color_b'] = value_color[2]

    df = df.astype({"value_color_r": int, "value_color_g": int, "value_color_b": int})

    # save back to csv file
    df.to_csv(csv_file, index=False)
    return df


def scatter_chart(chemistry, df, elevation=None, azimuth=None):
    fig = plt.figure(figsize=(30, 18))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('$RED$', fontsize=15)
    ax.set_ylabel('$GREEN$', fontsize=15, rotation=150)
    ax.set_zlabel('$BLUE$', fontsize=15, rotation=50)

    plt.title(label=chemistry, fontsize=40, color="gray")
    # sequence line
    ax.plot3D(df['value_color_r'], df['value_color_g'], df['value_color_b'], 'gray')

    colors_hex = ['#%02x%02x%02x' % (df.at[i, 'value_color_r'],
                                     df.at[i, 'value_color_g'],
                                     df.at[i, 'value_color_b']) for i in df.index]
    ax.scatter(df['value_color_r'], df['value_color_g'], df['value_color_b'],
               c=colors_hex, s=200, marker='D')

    for i in df.index:
        ax.text(df.at[i, 'value_color_r'],
                df.at[i, 'value_color_g'],
                df.at[i, 'value_color_b'],
                f"{df.at[i, 'actual_value']}", size=8, zorder=10, color='k',
                # f"{df.at[i, 'actual_value']}_{df.at[i, 'file_path']}", size=8, zorder=10, color='k'
                )

    ax.view_init(elevation, azimuth)
    plt.savefig(f'{chemistry}_scatter.png')
    plt.show()
    return ax
