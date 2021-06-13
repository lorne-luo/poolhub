import os
from decimal import Decimal

import joblib
import keras
import numpy as np
import rpyc

from core.constants import ColorFormat

current_folder = os.path.dirname(os.path.realpath(__file__))
model_root = os.path.join(current_folder, 'model_save/one_hidden_layer2/')

model_versions = {
    # th
    'th_rgb': 'th_rgb_210613_32x256_0.001104',
    'th_hsv': 'th_hsv_210613_128x128_0.001876',
    # tc
    'tc_rgb': 'tc_rgb_210613_256x16_0.179485',
    'tc_hsv': '',
    # fc
    'fc_rgb': 'fc_rgb_210613_128x8_0.103663',
    'fc_hsv': '',
    # ph
    'ph_rgb': 'ph_rgb_210613_64x32_0.300377',
    'ph_hsv': 'ph_hsv_210612_8x64_0.30311',
    # ta
    'ta_rgb': 'ta_rgb_210613_128x64_0.443088',
    'ta_hsv': '',
    # ca
    'ca_rgb': 'ca_rgb_210613_256x256_0.472354',
    'ca_hsv': '',
}
release_models = {}


def load_model(chemistry, color_format):
    model_key = f"{chemistry}_{color_format}"
    model = release_models.get(model_key, None)
    if model:
        return model

    model_name = model_versions[model_key]
    model_path = os.path.join(model_root, model_name)
    model = keras.models.load_model(model_path)
    scaler_path = os.path.join(model_path, 'scaler.joblib')
    scaler = joblib.load(scaler_path)
    release_models[model_key] = model, scaler
    return model, scaler


def predict(chemistry, color, color_format=ColorFormat.RGB):
    """predict value from color"""
    scaled_color = np.array([color])
    if color_format == ColorFormat.RGB:
        scaled_color = scaled_color / 255

    print(scaled_color)
    model, scaler = load_model(chemistry, color_format)

    prediction = model.predict(scaled_color)
    scaled_prediction = scaler.inverse_transform(prediction)
    return Decimal(str(scaled_prediction[0][0])).quantize(Decimal('1.00'))


def predict_one(chemistry, color, color_format=ColorFormat.RGB):
    client = rpyc.connect("localhost", 18861)
    prediction = client.predict(chemistry, color, color_format)
    client.close()
    return prediction


def predict_all(colors: dict, color_format=ColorFormat.RGB):
    client = rpyc.connect("localhost", 18861)
    result = {}
    for chemistry, color in colors.items():
        prediction = client.predict(chemistry, color, color_format)
        result[chemistry] = prediction
    client.close()
    return result
