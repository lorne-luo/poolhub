import os
from datetime import datetime
from decimal import Decimal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Make numpy printouts easier to read.
from numpy.random.mtrand import RandomState
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from IPython.display import clear_output

from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler, Normalizer
from tensorflow.python.keras.layers import Dense

from core.constants import ColorFormat

np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf

from tensorflow import keras

model_folder = '/Users/lorneluo/lorne/poolhub/apps/color_band_training/model_save/one_hidden_layer2'
csv_base_path = '/Users/lorneluo/lorne/poolhub/dataset/debug/annotation/'
hsv_csv_path = os.path.join(csv_base_path, 'hsv_value.csv')
rgb_csv_path = os.path.join(csv_base_path, 'rgb_value.csv')


def normalize_value(chemistry, y_train, y_test):
    """return scaled y_train, scaled y_test and inverse_transform"""
    if chemistry in ['th', 'tc', 'fc', 'ph', 'ta', 'ca']:
        scaler = StandardScaler()
        scaler.fit(y_train)
        ytrain_scale = scaler.transform(y_train)
        ytest_scale = scaler.transform(y_test)
        return ytrain_scale, ytest_scale, scaler
    raise Exception('No Normalization specified')


def get_train_data(chemistry, color_format):
    # 1. read data
    csv_path = os.path.join(csv_base_path, f'{color_format}_value.csv')
    dataset = pd.read_csv(csv_path)
    train_dataset = dataset[pd.notna(dataset[f"{chemistry}_value"])]
    # test_dataset = train_dataset.sample(frac=0.2, random_state=RandomState())
    test_dataset = train_dataset
    # print(min(train_dataset[f"{chemistry}_value"]), max(train_dataset[f"{chemistry}_value"]))

    # 2. split train and test data
    X_train = train_dataset[[f"{chemistry}_color_{color_format[0]}",
                             f"{chemistry}_color_{color_format[1]}",
                             f"{chemistry}_color_{color_format[2]}"]]
    y_train = train_dataset[f"{chemistry}_value"]
    X_test = test_dataset[[f"{chemistry}_color_{color_format[0]}",
                           f"{chemistry}_color_{color_format[1]}",
                           f"{chemistry}_color_{color_format[2]}"]]
    y_test = test_dataset[f"{chemistry}_value"]
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    # 3. normalization
    Xtrain_scaled = X_train.to_numpy()
    Xtest_scaled = X_test.to_numpy()
    if color_format == ColorFormat.RGB:
        Xtrain_scaled = Xtrain_scaled / 255
        Xtest_scaled = Xtest_scaled / 255
    y_train = np.reshape(y_train, (-1, 1))
    y_test = np.reshape(y_test, (-1, 1))
    ytrain_scaled, ytest_scaled, scaler = normalize_value(chemistry, y_train, y_test)
    # print(ytest_scale)
    # print(scaler.inverse_transform(ytest_scale))
    # return 1, 1
    return X_test, y_test, Xtrain_scaled, ytrain_scaled, Xtest_scaled, ytest_scaled, scaler


def training_model(chemistry, color_format, model_folder=model_folder):
    X_test, y_test, Xtrain_scaled, ytrain_scaled, Xtest_scaled, ytest_scaled, scaler = get_train_data(chemistry,
                                                                                                      color_format)

    print(len(X_test),len(y_test),len(Xtest_scaled),len(ytest_scaled))
    # 4. define model
    model = keras.Sequential()
    model.add(Dense(8, input_dim=3, activation='relu'))
    model.add(Dense(64, activation='relu'))
    # model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.summary()

    # 5. model training
    # optimizer: SGD, Adam, Adagrad, AdaDelta, RMSProp
    callback = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=100)
    model.compile(loss='mse', optimizer='adam', metrics=['mse'])
    history = model.fit(Xtrain_scaled, ytrain_scaled, epochs=3000, batch_size=32, callbacks=[callback],
                        verbose=0, validation_split=0.2)
    predictions = model.predict(Xtest_scaled)
    epochs = len(history.history['loss'])

    # 6.save model
    mse = mean_squared_error(ytest_scaled, predictions)
    layers_width = [str(layer.units) for layer in model.layers[:-1]]
    time_stamp = f"{datetime.now().strftime('%y%m%d')}"  # -%H%M%S
    model_path = os.path.join(model_folder,
                              f"{chemistry}_{color_format}_{time_stamp}_{'x'.join(layers_width)}_{round(mse, 6)}")
    model.save(model_path)
    scaler_path = os.path.join(model_path, 'scaler.joblib')
    joblib.dump(scaler, scaler_path)

    # 7. dump debug info
    fig = plt.figure(figsize=(15, 10))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig(os.path.join(model_path, 'loss.jpg'))

    predictions = np.array(predictions)
    predictions = np.reshape(predictions, (-1, 1))
    predictions = scaler.inverse_transform(predictions)
    with open(os.path.join(model_path, 'test_prediction.txt'), 'a') as file_handler:
        for i, val in enumerate(predictions):
            pre_value = round(float(val), 2)
            file_handler.write(
                f'{X_test.to_numpy()[i]} | {pre_value} -> {y_test[i]} = {round(float(y_test[i] - pre_value), 2)}\n')

    return mse, epochs, model_path


def load_model(model_folder):
    scaler_path = os.path.join(model_folder, 'scaler.joblib')
    scaler = joblib.load(scaler_path)
    model = keras.models.load_model(model_folder)
    return model, scaler


def predict(color,color_format=ColorFormat.RGB):
    scaled_color = np.array([color])
    if color_format == ColorFormat.RGB:
        scaled_color = scaled_color / 255
    base_folder = '/Users/lorneluo/lorne/poolhub/apps/color_band_training/model_save/one_hidden_layer2/'
    rgb_model_folder = os.path.join(base_folder, 'ph_rgb_210612-171308_16_0.35155')
    hsv_model_folder = os.path.join(base_folder, 'ph_hsv_210612-171713_16_0.67437')
    model_folder = rgb_model_folder if color_format.lower() == ColorFormat.RGB else hsv_model_folder

    model, scaler = load_model(model_folder)
    prediction = model.predict(scaled_color)
    scaled_prediction = scaler.inverse_transform(prediction)
    return Decimal(str(scaled_prediction[0][0])).quantize(Decimal('1.00'))


if __name__ == '__main__':
    pass
    # from apps.color_band_training import ann_prediction
    #
    # reload(ann_prediction)
    # mses = []
    # epochs = []
    # for i in range(1):
    #     mse, epoch,_ = ann_prediction.training_model('ph', 'hsv')
    #     mses.append(mse)
    #     epochs.append(epoch)
    #     print(f'MSE = {mse}')
    # print(mses, sum(mses) / len(mses))
    # print(epochs, sum(epochs) / len(epochs))

    # color = [144, 25, 26]
    # from apps.color_band_training import ann_prediction
    # reload(ann_prediction)
    # rgb_prediction = ann_prediction.predict('rgb', color)
    # hsv_prediction = ann_prediction.predict('hsv', color)
    # print(rgb_prediction, hsv_prediction)
