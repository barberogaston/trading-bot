from fastapi import FastAPI
from keras.models import load_model

from trading_bot.agent import huber_loss


app = FastAPI()
model = load_model('model.keras', {"huber_loss": huber_loss})


@app.get('/ping')
def ping():
    return 'pong'
