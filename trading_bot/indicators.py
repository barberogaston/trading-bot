import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD, SMAIndicator
from ta.volume import (ChaikinMoneyFlowIndicator, MFIIndicator,
                       OnBalanceVolumeIndicator)


def add_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Adds the indicators consumed by the bot.

    Parameters
    ----------
    data : pd.DataFrame
        A dataframe with daily stock values. Must include: open, high,
        low, close and volume. It should also be sorted in a descending
        manner.

    Returns
    -------
    pd.DataFrame
        The input dataframe with the indicators added.
    """
    data = data.copy()
    rsi = RSIIndicator(data['close'])
    ema = EMAIndicator(data['close'])
    sma = SMAIndicator(data['close'], n=14)
    macd = MACD(data['close'])
    chaikin = ChaikinMoneyFlowIndicator(data['high'], data['low'],
                                        data['close'], data['volume'])
    mfi = MFIIndicator(data['high'], data['low'], data['close'],
                       data['volume'])
    obv = OnBalanceVolumeIndicator(data['close'], data['volume'])

    data.loc[:, 'rsi'] = rsi.rsi()
    data.loc[:, 'ema'] = ema.ema_indicator()
    data.loc[:, 'sma'] = sma.sma_indicator()
    data.loc[:, 'macd'] = macd.macd()
    data.loc[:, 'macd_diff'] = macd.macd_diff()
    data.loc[:, 'macd_signal'] = macd.macd_signal()
    data.loc[:, 'chaikin'] = chaikin.chaikin_money_flow()
    data.loc[:, 'mfi'] = mfi.money_flow_index()
    data.loc[:, 'obv'] = obv.on_balance_volume()

    return data
