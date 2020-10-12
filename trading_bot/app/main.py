import numpy as np
import pandas as pd
from fastapi import FastAPI
from keras.models import load_model

from trading_bot.agent import huber_loss
from trading_bot.indicators import add_indicators
from trading_bot.ops import get_state
from trading_bot.utils import filter_data_by_feature_columns


app = FastAPI()
model = load_model('model.keras', {"huber_loss": huber_loss})
bitcoin = pd.read_csv('bitcoin.csv')


@app.get('/ping')
def ping():
    return 'pong'


@app.get('/action')
def action():
    actions = ['HOLD', 'BUY', 'SELL']
    data = filter_data_by_feature_columns(add_indicators(bitcoin))
    state = get_state(data, data.shape[0] - 1, 16)
    action_probs = model.predict(state)
    return actions[np.argmax(action_probs[0])]
