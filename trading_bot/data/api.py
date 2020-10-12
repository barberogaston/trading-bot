import pandas as pd

from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def get_current_data() -> pd.DataFrame:
    """Return a DataFrame with the current bitcoin data.

    Returns
    -------
    pd.DataFrame
        Current bitcoin data.
    """
    data = {'close': [get_current_price()],
            'volume': [get_24h_volume()],
            'high': [get_24h_high()],
            'low': [get_24h_low()]}
    return pd.DataFrame(data)


def get_current_price() -> float:
    """Get the current price in USD.

    Returns
    -------
    float
        Current Bitcoin price.
    """
    response = cg.get_price(ids='bitcoin', vs_currencies='usd')
    return response['bitcoin']['usd']


def get_24h_volume() -> float:
    """Get the 24 hour volume in USD.

    Returns
    -------
    float
        24 hour volume in USD.
    """
    response = cg.get_price(ids='bitcoin', vs_currencies='usd',
                            include_24hr_vol='true')
    return response['bitcoin']['usd_24h_vol']


def get_24h_high() -> float:
    """Get the 24 hour high in USD.

    Returns
    -------
    float
        24 hour high in USD.
    """
    response = cg.get_coin_by_id(id='bitcoin', localization='false',
                                 tickers='false', community_data='false',
                                 developer_data='false', sparkline='false')
    return response['market_data']['high_24h']['usd']


def get_24h_low() -> float:
    """Get the 24 hour low in USD.

    Returns
    -------
    float
        24 hour low in USD.
    """
    response = cg.get_coin_by_id(id='bitcoin', localization='false',
                                 tickers='false', community_data='false',
                                 developer_data='false', sparkline='false')
    return response['market_data']['low_24h']['usd']
