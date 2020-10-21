import numpy as np
import pandas as pd
from fastapi import FastAPI
from keras.models import load_model

from trading_bot.app.utils import get_action
from trading_bot.agent import huber_loss
from trading_bot.indicators import add_indicators
from trading_bot.ops import get_state
from trading_bot.utils import filter_data_by_feature_columns


app = FastAPI()
model = load_model('/data/model', {"huber_loss": huber_loss})
bitcoin = pd.read_csv('/data/bitcoin.csv')


@app.get('/ping')
def ping():
    return 'pong'


@app.get('/action')
def action():
    actions = ['HOLD', 'BUY', 'SELL']
    action_date = bitcoin.iloc[-1].loc['date']
    close_price = bitcoin.iloc[-1].loc['close']
    data = filter_data_by_feature_columns(add_indicators(bitcoin))
    state = get_state(data, data.shape[0] - 1, 16)
    action_probs = (
        dict(zip(actions, [float(prob) for prob in model.predict(state)[0]])))
    action = get_action(action_probs)
    action_probs['ADJUSTED_SELL'] = action_probs['SELL'] * 0.98
    response = {
        'action': action,
        'date': action_date,
        'close': close_price,
        'probs': action_probs
    }
    return response
