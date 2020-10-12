import os
import requests
from datetime import datetime
from logging import getLogger

import pandas as pd


here = os.path.abspath(os.path.dirname(__file__))
logger = getLogger(__name__)
root = os.path.dirname(os.path.abspath(__file__))
now = str(int(datetime.now().timestamp()))
url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical'
date_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'

params = {'convert': 'USD',
          'time_end': now,
          'time_start': '1367020800'}

coin = 'bitcoin'
params['slug'] = coin
res = requests.get(url, params=params)
data = res.json().get('data', None)
if data:
    historical = pd.DataFrame(
        [item['quote']['USD'] for item in data['quotes']])
    historical.loc[:, 'date'] = (
        historical['timestamp'].apply(
            lambda d: datetime.strptime(d, date_fmt).date()))
    historical.to_csv(f'{here}/{coin}.csv', index=False)
else:
    logger.error(f'Retrieving {coin} data failed.')
    logger.error(res.text)
