import csv
import os
import sys
from datetime import datetime
from itertools import permutations, product
from multiprocessing import Pool, cpu_count
import joblib
import keras
import pandas as pd
import numpy as np
from numpy.random.mtrand import RandomState
from tensorflow.python.keras.layers import Dense
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

from apps.color_band_training.ann_prediction import normalize_value, get_train_data
from core.constants import ColorFormat

model_folder = '/Users/lorneluo/lorne/poolhub/apps/color_band_training/model_save/tuning'


def build_model(*layer_numbers):
    model = keras.Sequential()
    model.add(Dense(layer_numbers[0], input_dim=3, activation='relu'))
    for n in layer_numbers[1:]:
        model.add(Dense(n, activation='relu'))
    model.add(Dense(1, activation='linear'))
    # model.summary()
    return model


def main(chemistry, color_format, start, end):
    X_test, y_test, Xtrain_scaled, ytrain_scaled, Xtest_scaled, ytest_scaled, scaler = get_train_data(chemistry,
                                                                                                      color_format)

    layer_numbers = [8, 16, 32, 64, 128, 256]
    layer_combinations = list(product(layer_numbers, repeat=2))  # + list(product(layer_numbers, 3))

    trains_csv = os.path.join(model_folder, f'trains_{chemistry}_{color_format}.csv')
    params_csv = os.path.join(model_folder, f'params_{chemistry}_{color_format}.csv')
    # print(layer_combinations)

    for layers in layer_combinations[start:end]:
        mses = []
        epochs = []
        train_count = 10

        print_layers = (*layers, 0) if len(layers) < 3 else layers
        print('Start tunning', layers)
        for i in range(train_count):
            model = build_model(*layers)

            # 5. model training
            # optimizer: SGD, Adam, Adagrad, AdaDelta, RMSProp
            callback = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=0, patience=100)
            model.compile(loss='mse', optimizer='adam', metrics=['mse'])
            history = model.fit(Xtrain_scaled, ytrain_scaled, epochs=3000, batch_size=32, callbacks=[callback],
                                verbose=0, validation_split=0.2)
            predictions = model.predict(Xtest_scaled)
            epoch = len(history.history['loss'])

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

            print(layers, mse, epoch, model_path)
            with open(trains_csv, 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow((*print_layers, mse, epoch, model_path))

            mses.append(mse)
            epochs.append(epoch)

        print(*print_layers, sum(mses) / len(mses), sum(epochs) / len(epochs), train_count)
        with open(params_csv, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow((*print_layers, sum(mses) / len(mses), min(mses), max(mses), max(mses)-min(mses), sum(epochs) / len(epochs),
                             min(epochs), max(epochs), train_count))


if __name__ == '__main__':
    # def func(args):
    #     main(*args)
    # process_num = cpu_count() - 1
    # print('Process Pool =', process_num)
    # args = [('ph', 'rgb', i, process_num) for i in range(process_num)]
    # with Pool(processes=process_num) as pool:
    #     result=pool.map(func, args)

    # for i in range(process_num):
    #     start = int(36 / process_num * i)
    #     end = int(36 / process_num * (i + 1))
    #     print('python hyperparameter_tuning.py', start, end)
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    main('fc', 'rgb', start, end)


# python hyperparameter_tuning.py 0 5
# python hyperparameter_tuning.py 5 10
# python hyperparameter_tuning.py 10 15
# python hyperparameter_tuning.py 15 20
# python hyperparameter_tuning.py 20 25
# python hyperparameter_tuning.py 25 30
# python hyperparameter_tuning.py 30 36
