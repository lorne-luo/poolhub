import os
from decimal import Decimal
import numpy as np
import joblib
import keras
import rpyc

from rpyc.utils.server import ThreadedServer, OneShotServer

from core.constants import ColorFormat


class ColorPredictionService(rpyc.Service):
    model_root = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'apps/color_band_training/model_save/release/')
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

    def __init__(self):
        print(os.path.dirname(os.path.realpath(__file__)))
        print(self.model_root)
        super(ColorPredictionService, self).__init__()
        for model_key, model_version in self.model_versions.items():
            if not model_version:
                continue
            model_path = os.path.join(self.model_root, model_version)
            model = keras.models.load_model(model_path)
            scaler_path = os.path.join(model_path, 'scaler.joblib')
            scaler = joblib.load(scaler_path)
            self.release_models[model_key] = model, scaler

        print(f'Prediction model loaded: {list(self.release_models.keys())}')

    def get_model(self, chemistry, color_format):
        model_key = f"{chemistry.lower()}_{color_format}"
        model, scaler = self.release_models.get(model_key, (None, None))
        if model and scaler:
            return model, scaler

        model_name = self.model_versions[model_key]
        model_path = os.path.join(self.model_root, model_name)
        model = keras.models.load_model(model_path)
        scaler_path = os.path.join(model_path, 'scaler.joblib')
        scaler = joblib.load(scaler_path)
        self.release_models[model_key] = model, scaler
        return model, scaler

    def exposed_predict(self, chemistry, color, color_format=ColorFormat.RGB):
        """predict value from color"""
        scaled_color = np.array([color])
        if color_format == ColorFormat.RGB:
            scaled_color = scaled_color / 255

        model, scaler = self.get_model(chemistry, color_format)
        prediction = model.predict(scaled_color)
        scaled_prediction = scaler.inverse_transform(prediction)
        return Decimal(str(scaled_prediction[0][0])).quantize(Decimal('1.00'))

    def exposed_get_answer(self):  # this is an exposed method
        return 42


if __name__ == "__main__":
    t = ThreadedServer(ColorPredictionService(), port=18861)
    print('Service running.')
    t.start()
