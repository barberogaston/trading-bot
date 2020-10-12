import os
import requests
from datetime import datetime, date
from logging import getLogger

import pandas as pd


def parse_api_timestamp_to_date(timestamp: str) -> date:
    """Converts the string timestamp to a python date object.

    Parameters
    ----------
    timestamp : str
        API's timestamp string.

    Returns
    -------
    date
        Extracted date from the timestamp.
    """
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(timestamp, date_format).date()


# This folder
here = os.path.abspath(os.path.dirname(__file__))

# API call params
coin = 'bitcoin'
params = {'convert': 'USD',
          'time_end': str(int(datetime.now().timestamp())),  # Now
          'time_start': '1367020800',
          'slug': coin}

# Make API call
url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical'
res = requests.get(url, params=params)
data = res.json().get('data', None)

if data:
    # Convert API response to DataFrame
    json_list = [item['quote']['USD'] for item in data['quotes']]
    historical = pd.DataFrame(json_list)

    # Parse timestamp to date
    historical.loc[:, 'date'] = (
        historical['timestamp'].apply(parse_api_timestamp_to_date))

    # Save to CSV
    historical.to_csv(f'{here}/{coin}.csv', index=False)
else:
    # Log error from API
    logger = getLogger(__name__)
    logger.error(f'Retrieving {coin} data failed.')
    logger.error(res.text)
