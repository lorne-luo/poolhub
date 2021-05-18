# Some basic setup:
import os
import glob
from pathlib import Path
# Setup detectron2 logger
from pprint import pprint
import detectron2
import torch
from detectron2.utils.logger import setup_logger
from PIL import Image

setup_logger()

import numpy as np
import cv2

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import ColorMode
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.detection_utils import read_image


def inference(input_img, output_img=None):
    """
    model training
    https://colab.research.google.com/drive/1k6aD5zgSn47qWuIznU_QamVkTINVVL0i?authuser=1#scrollTo=y4uUVL_CGOCg
    """

    # Inference should use the config with parameters that are used in training
    # cfg now already contains everything we've set previously. We changed it a little bit for inference:
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
    # get metadata
    # metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])

    img = cv2.imread(input_img)
    outputs = predictor(img)
    v = Visualizer(img[:, :, ::-1],
                   scale=0.5,
                   instance_mode=ColorMode.IMAGE_BW
                   # remove the colors of unsegmented pixels. This option is only available for segmentation models
                   )
    cpu_output = outputs["instances"].to("cpu")
    out = v.draw_instance_predictions(cpu_output)
    if output_img:
        cv2.imwrite(output_img, out.get_image()[:, :, ::-1])

    scores = cpu_output.scores.numpy()
    boxes = cpu_output.pred_boxes.tensor.numpy()
    return scores, boxes


def verify_inference():
    output_folder = '/Users/lorneluo/lorne/poolhub/dataset/inference'
    train_folder = '/Users/lorneluo/lorne/poolhub/dataset/white_balanced/'
    all_images = glob.glob(f'{train_folder}*.jpg') + glob.glob(f'{train_folder}*.jpeg')+ glob.glob(f'{train_folder}*.png')

    for img_path in all_images:
        filename = os.path.basename(img_path)
        output_img = os.path.join(output_folder, filename)
        scores, boxes = inference(img_path, output_img)

        score = scores[0]
        new_path = os.path.join(output_folder, f'{score:.2f}_{filename}')

        os.rename(output_img, new_path)
        print(filename, scores, boxes)
