import math

import numpy as np


def sigmoid(x):
    """Performs sigmoid operation."""
    try:
        if x < 0:
            return 1 - 1 / (1 + math.exp(x))
        return 1 / (1 + math.exp(-x))
    except Exception as err:
        print("Error in sigmoid: " + err)


def get_state(complete_data, current_time, n_days):
    """Returns an n-day state representation ending at time t."""
    time_from = current_time - n_days + 1
    res = []
    feature_columns = ['close', 'rsi', 'ema', 'sma', 'macd', 'macd_signal',
                       'macd_diff', 'volume', 'chaikin', 'mfi', 'obv']

    for col in feature_columns:
        data = complete_data.loc[:, col].tolist()
        block = (
            data[time_from: current_time + 1]
            if time_from >= 0
            else -time_from * [data[0]] + data[0: current_time + 1]
        )
        for i in range(n_days - 1):
            res.append(sigmoid(block[i + 1] - block[i]))
    return np.array([res])
