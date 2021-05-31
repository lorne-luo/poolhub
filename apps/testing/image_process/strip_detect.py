import os
import glob
from datetime import datetime

import torch
import cv2
import csv
import numpy as np
from csv import reader
from pathlib import Path

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import ColorMode
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.detection_utils import read_image

from apps.testing.image_process.pre_process import crop_area, pick_average_color2, white_balance2


def get_predictor():
    cfg = get_cfg()
    model_config = 'mask_rcnn_R_50_FPN_3x.yaml'
    cfg.merge_from_file(model_zoo.get_config_file(f"COCO-InstanceSegmentation/{model_config}"))
    if torch.cuda.is_available():
        cfg.MODEL.DEVICE = "cuda"
    else:
        # set device to cpu
        cfg.MODEL.DEVICE = "cpu"
    current_folder = Path(__file__).resolve().parent
    model_path = current_folder.joinpath('output/model_final.pth')
    cfg.MODEL.WEIGHTS = str(model_path)
    # print(cfg.MODEL.WEIGHTS)
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set a custom testing threshold
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg.TEST.DETECTIONS_PER_IMAGE = 1
    predictor = DefaultPredictor(cfg)
    return predictor


def inference(input_img, output_folder=None):
    """
    model training
    https://colab.research.google.com/drive/1k6aD5zgSn47qWuIznU_QamVkTINVVL0i?authuser=1#scrollTo=y4uUVL_CGOCg
    """

    # Inference should use the config with parameters that are used in training
    # cfg now already contains everything we've set previously. We changed it a little bit for inference:
    predictor = get_predictor()
    # get metadata
    # metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
    if isinstance(input_img, str):
        file_name = os.path.basename(input_img)
        img = cv2.imread(input_img)
    else:
        file_name = datetime.now().strftime('%Y-%m-%d %H%M%S%f')
        img = input_img

    outputs = predictor(img)
    v = Visualizer(img[:, :, ::-1],
                   scale=1,
                   instance_mode=ColorMode.IMAGE_BW
                   # remove the colors of unsegmented pixels. This option is only available for segmentation models
                   )
    cpu_output = outputs["instances"].to("cpu")
    out = v.draw_instance_predictions(cpu_output)
    if output_folder:
        output_img = os.path.join(output_folder, file_name)
        cv2.imwrite(output_img, out.get_image()[:, :, ::-1])

    scores = cpu_output.scores.numpy()
    boxes = cpu_output.pred_boxes.tensor.numpy()
    return scores, boxes, img


def bulk_inference(input_imgs, output_folder=None):
    predictor = get_predictor()
    result = []
    for input_img in input_imgs:

        if isinstance(input_img, str):
            file_name = os.path.basename(input_img)
            img = cv2.imread(input_img)
        else:
            file_name = datetime.now().strftime('%Y-%m-%d %H%M%S%f')
            img = input_img

        outputs = predictor(img)
        v = Visualizer(img[:, :, ::-1],
                       scale=1,
                       instance_mode=ColorMode.IMAGE_BW)
        cpu_output = outputs["instances"].to("cpu")
        out = v.draw_instance_predictions(cpu_output)
        if output_folder:
            output_img = os.path.join(output_folder, file_name)
            cv2.imwrite(output_img, out.get_image()[:, :, ::-1])

        scores = cpu_output.scores.numpy()
        boxes = cpu_output.pred_boxes.tensor.numpy()
        return result.append((scores, boxes, img))


def verify_inference():
    """verify inference, save pic to ingerence folder"""
    output_folder = '/Users/lorneluo/lorne/poolhub/dataset/inference'
    train_folder = '/Users/lorneluo/lorne/poolhub/dataset/white_balanced/'
    all_images = glob.glob(f'{train_folder}*.jpg') + glob.glob(f'{train_folder}*.jpeg') + glob.glob(
        f'{train_folder}*.png')

    for img_path in all_images:
        filename = os.path.basename(img_path)
        output_img = os.path.join(output_folder, filename)
        scores, boxes, _ = inference(img_path, output_img)
        if not len(scores):
            print(f'{img_path} not detected.')
            continue
        score = scores[0]
        new_path = os.path.join(output_folder, f'{score:.2f}_{filename}')

        os.rename(output_img, new_path)
        # print(filename, scores, boxes)


def detect_strip(input_path, output_path=None):
    """detect strip and save cropped image to output folder
    input_path='/Users/lorneluo/lorne/poolhub/dataset/white_balanced/File_003.jpeg'
    output_folder='/Users/lorneluo/lorne/poolhub/dataset/crop'
    detect_strip(input_path,output_folder)
    """
    filename = os.path.basename(input_path)
    scores, boxes, image = inference(input_path)
    if not len(scores):
        print(f'No strip detected.')
        return None, None, None

    max_score = max(scores)
    max_index = np.where(scores == max_score)[0][0]
    max_box = boxes[max_index]
    # print(max_score, max_box)

    height = int(max_box[3] - max_box[1])
    width = int(max_box[2] - max_box[0])
    top_left_x = int(max_box[1] - width) if max_box[1] > width else int(max_box[1])
    top_left = (top_left_x, int(max_box[0]))
    bottom_right = (int(max_box[3]) + width * 3, int(max_box[2]))

    # print(top_left[0], bottom_right[0], top_left[1], bottom_right[1])
    # print(width, height)
    crop_img = image[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
    # print(crop_img)
    # print(crop_img.shape)

    if output_path:
        cv2.imwrite(output_path, crop_img)
    return max_score, max_box, crop_img


def locate_strip_points(strip_img, filename=None):
    """
    1. locate top and bottom of strip
    2. calculate 7 color points
    3. white balance
    """
    height = strip_img.shape[0]
    width = strip_img.shape[1]

    x = int(width / 2)
    top_y, bottom_y = 0, height

    # find top edge
    for i in range(height):
        is_first_color = [150 < sum(strip_img[i + j, x]) < 380 for j in range(16)]
        if sum(is_first_color) > 12:
            top_y = i
            break

    # find bottom edge
    for i in range(height):
        y = height - 1 - i
        is_last_color = [150 < sum(strip_img[y - j, x]) < 330 for j in range(16)]
        if sum(is_last_color) > 12:
            bottom_y = y
            break
    # print(top_y, bottom_y)

    # white balance
    wb_y = int((top_y + bottom_y) / 2)
    # print(top_y, bottom_y, wb_y)
    strip_img, _ = white_balance2(strip_img, (x, wb_y))

    # y of 7 color position
    y_factors = [0.04183813443072702,
                 0.2199917695473251,
                 0.4051769547325103,
                 0.5899903978052127,
                 0.7782908093278463,
                 0.9574759945130316]
    # white balance point

    height = bottom_y - top_y
    y_list = [int(height * i + top_y) for i in y_factors]

    # if output_path:
    #     cv2.imwrite(output_path, strip_img)
    #     folder, ext = os.path.splitext(file_name)
    #
    #     output_path = f'{folder[:-2]}.3.{ext}'

    # 7 color's coordinate
    color_points = [(x, y) for y in y_list]
    wb_xy = (x, wb_y)
    top_bottom_edges = (top_y, bottom_y)
    return top_bottom_edges, color_points, wb_xy


def pick_colors(strip_img, color_points, top_bottom_edges, wb_xy, output_path=None):
    """white balance first and pick colors"""
    top_y, bottom_y = top_bottom_edges
    height = strip_img.shape[0]
    width = strip_img.shape[1]
    middle_x = int(width / 2)
    strip_img, _ = white_balance2(strip_img, wb_xy)

    colors = []
    # print(color_points)
    for x, y in color_points:
        color = pick_average_color2(strip_img, (x, y))
        colors.append(color)
        if output_path:
            strip_img = cv2.drawMarker(strip_img, (x, y), color=(0, 255, 0), markerType=cv2.MARKER_CROSS,
                                       markerSize=32, thickness=2)

    if output_path:
        # middle wb point
        strip_img = cv2.drawMarker(strip_img, wb_xy, color=(0, 255, 0), markerType=cv2.MARKER_DIAMOND,
                                   markerSize=32, thickness=2)
        # top
        strip_img = cv2.drawMarker(strip_img, (middle_x, top_y), color=(0, 255, 0), markerType=cv2.MARKER_DIAMOND,
                                   markerSize=32, thickness=2)
        # bottom
        strip_img = cv2.drawMarker(strip_img, (middle_x, bottom_y), color=(0, 255, 0), markerType=cv2.MARKER_DIAMOND,
                                   markerSize=32, thickness=2)
        cv2.imwrite(output_path, strip_img)
    return colors


def pick_strip_color(strip_img, filename=None, output_path=None):
    """pick 7 colors from cropped strip img"""
    height = strip_img.shape[0]
    width = strip_img.shape[1]

    x = int(width / 2)
    top_y, bottom_y = 0, height

    # find top edge
    for i in range(height):
        is_first_color = [150 < sum(strip_img[i + j, x]) < 380 for j in range(16)]
        if sum(is_first_color) > 12:
            top_y = i
            break

    # find bottom edge
    for i in range(height):
        y = height - 1 - i
        is_last_color = [150 < sum(strip_img[y - j, x]) < 330 for j in range(16)]
        if sum(is_last_color) > 12:
            bottom_y = y
            break
    # print(top_y, bottom_y)

    # white balance
    wb_y = int((top_y + bottom_y) / 2)
    # print(top_y, bottom_y, wb_y)
    strip_img, _ = white_balance2(strip_img, (x, wb_y))

    # y of 7 color position
    y_factors = [0.04183813443072702,
                 0.2199917695473251,
                 0.4051769547325103,
                 0.5899903978052127,
                 0.7782908093278463,
                 0.9574759945130316]
    # white balance point

    height = bottom_y - top_y
    y_list = [int(height * i + top_y) for i in y_factors]

    # if output_path:
    #     cv2.imwrite(output_path, strip_img)
    #     folder, ext = os.path.splitext(file_name)
    #
    #     output_path = f'{folder[:-2]}.3.{ext}'

    # 7 color's coordinate
    colors = []
    color_points = [(x, y) for y in y_list]
    # print(color_points)
    for x, y in color_points:
        color = pick_average_color2(strip_img, (x, y))
        colors.append(color)
        if output_path:
            strip_img = cv2.drawMarker(strip_img, (x, y), color=(0, 255, 0), markerType=cv2.MARKER_CROSS,
                                       markerSize=32, thickness=2)

    if output_path:
        # middle wb point
        strip_img = cv2.drawMarker(strip_img, (x, wb_y), color=(0, 255, 0), markerType=cv2.MARKER_DIAMOND,
                                   markerSize=32, thickness=2)
        # top
        strip_img = cv2.drawMarker(strip_img, (x, top_y), color=(0, 255, 0), markerType=cv2.MARKER_DIAMOND,
                                   markerSize=32, thickness=2)
        # bottom
        strip_img = cv2.drawMarker(strip_img, (x, bottom_y), color=(0, 255, 0), markerType=cv2.MARKER_DIAMOND,
                                   markerSize=32, thickness=2)
        cv2.imwrite(output_path, strip_img)
    return colors


def test_color_pick():
    csv_path = '/Users/lorneluo/lorne/poolhub/apps/color_band_training/ph.csv'
    base_folder = '/Users/lorneluo/lorne/poolhub/dataset/train/'
    debug_folder = '/Users/lorneluo/lorne/poolhub/dataset/debug/'
    output_csv_path = os.path.join('/Users/lorneluo/lorne/poolhub/dataset/csv',
                                   f"{datetime.now().strftime('%Y-%m-%d %H%M%S')}.csv")
    file_names = []

    with open(csv_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader, None)  # skip the headers
        for row in csv_reader:
            file_names.append(row[0])

    # write colors into csv
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write header
        writer.writerow(['path', 'top_y', 'bottom_y', 'wb_y', 'wb_y',
                         'th_color', 'tc_color', 'fc_color', 'ph_color', 'ta_color', 'ca_color'])

        for file_name in file_names:
            file_path = os.path.join(base_folder, file_name)
            name, ext = os.path.splitext(file_name)

            try:
                #debug_img_path1 = os.path.join(debug_folder, f'{name}.1{ext}')
                debug_img_path1 = None
                max_score, max_box, crop_img = detect_strip(file_path,
                                                            debug_img_path1)
                if max_score:
                    print(file_path)
                    debug_img_path2 = os.path.join(debug_folder, f'{name}.2{ext}')
                    top_bottom_edges, color_points, wb_point = locate_strip_points(crop_img, file_name)
                    colors = pick_colors(crop_img, color_points, top_bottom_edges, wb_point,
                                         debug_img_path2)
                    print(colors)
                    writer.writerow(
                        [debug_img_path2, top_bottom_edges[0], top_bottom_edges[1], wb_point[0], wb_point[1],
                         str(colors[0]), str(colors[1]), str(colors[2]), str(colors[3]), str(colors[4]),
                         str(colors[5])]
                    )
                else:
                    print('No strip found', file_path)
            except Exception as ex:
                print('Error', file_path, ex)


def test_single_color(file_path):
    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)

    debug_folder = '/Users/lorneluo/lorne/poolhub/dataset/debug/'

    strip_crop_save = os.path.join(debug_folder, f'{name}.1{ext}')

    max_score, max_box, crop_img = detect_strip(file_path, strip_crop_save)
    if max_score:
        print(file_path)
        strip_color_save = os.path.join(debug_folder, f'{name}.2{ext}')
        colors = pick_strip_color(crop_img, file_name, strip_color_save)
        print(colors)
    else:
        print('No strip found', file_path)


def export_training_csv():
    pass
