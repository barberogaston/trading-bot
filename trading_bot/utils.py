import os
import logging

import pandas as pd

import keras.backend as K


# Formats Position
def format_position(price):
    return ('-$' if price < 0 else '+$') + '{0:.2f}'.format(abs(price))


# Formats Currency
def format_currency(price):
    return '${0:.2f}'.format(abs(price))


def show_train_result(result, val_position):
    """ Displays training results."""
    logging.info('Episode {}/{} - '
                 'Train Position: {}  '
                 'Val Position: {}  Train Loss: {:.4f})'
                 .format(result[0], result[1], format_position(result[2]),
                         format_position(val_position), result[3]))
    with open('train_result.csv', 'a+') as f:
        f.write(f'{result[0]},{result[2]}, {val_position},{result[3]}\n')


def show_eval_result(model_name, profit, first_buy):
    """ Displays eval results."""
    total_profit = format_position(profit)
    roi = round(profit / first_buy * 100, 2)
    logging.info(f'{model_name}: {total_profit} ({roi}%)\n')


def get_stock_data(stock_file):
    """Reads stock data from csv file."""
    return pd.read_csv(stock_file)


def switch_k_backend_device():
    """ Switches `keras` backend from GPU to CPU if required.

    Faster computation on CPU (if using tensorflow-gpu).
    """
    if K.backend() == "tensorflow":
        logging.debug("switching to TensorFlow for CPU")
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def filter_data_by_feature_columns(data):
    data = data.copy()
    feature_columns = ['close', 'rsi', 'ema', 'sma', 'macd', 'macd_signal',
                       'macd_diff', 'volume', 'chaikin', 'mfi', 'obv']
    return data.loc[:, feature_columns]
