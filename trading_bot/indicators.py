import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import (ADXIndicator, EMAIndicator, IchimokuIndicator, MACD,
                      SMAIndicator)
from ta.volatility import BollingerBands
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
    data = add_momentum_indicators(data)
    data = add_trend_indicators(data)
    data = add_volatility_indicators(data)
    data = add_volume_indicators(data)
    return data


def add_momentum_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Adds the momentum indicators.

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
    rsi = RSIIndicator(data['close'])
    stoch_osc = StochasticOscillator(data['high'], data['low'], data['close'])

    data.loc[:, 'rsi'] = rsi.rsi()
    data.loc[:, 'stoch_osc'] = stoch_osc.stoch()
    data.loc[:, 'stoch_osc_signal'] = stoch_osc.stoch_signal()

    return data


def add_trend_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Adds the trend indicators.

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
    adx = ADXIndicator(data['high'], data['low'], data['close'])
    ema = EMAIndicator(data['close'])
    ema_200 = EMAIndicator(data['close'], n=200)
    ichimoku = IchimokuIndicator(data['high'], data['low'])
    macd = MACD(data['close'])
    sma = SMAIndicator(data['close'], n=14)
    sma_200 = SMAIndicator(data['close'], n=200)

    data.loc[:, 'adx'] = adx.adx()
    data.loc[:, 'adx_pos'] = adx.adx_pos()
    data.loc[:, 'adx_neg'] = adx.adx_neg()
    data.loc[:, 'ema'] = ema.ema_indicator()
    data.loc[:, 'ema_200'] = ema_200.ema_indicator()
    data.loc[:, 'ichimoku_a'] = ichimoku.ichimoku_a()
    data.loc[:, 'ichimoku_b'] = ichimoku.ichimoku_b()
    data.loc[:, 'ichimoku_base_line'] = ichimoku.ichimoku_base_line()
    data.loc[:, 'ichimoku_conversion_line'] = (
        ichimoku.ichimoku_conversion_line())
    data.loc[:, 'macd'] = macd.macd()
    data.loc[:, 'macd_diff'] = macd.macd_diff()
    data.loc[:, 'macd_signal'] = macd.macd_signal()
    data.loc[:, 'sma'] = sma.sma_indicator()
    data.loc[:, 'sma_200'] = sma_200.sma_indicator()

    return data


def add_volatility_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Adds the volatility indicators.

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
    bb = BollingerBands(data['close'])

    data.loc[:, 'bollinger_hband'] = bb.bollinger_hband()
    data.loc[:, 'bollinger_hband_indicator'] = bb.bollinger_hband_indicator()
    data.loc[:, 'bollinger_lband'] = bb.bollinger_lband()
    data.loc[:, 'bollinger_lband_indicator'] = bb.bollinger_lband_indicator()
    data.loc[:, 'bollinger_mavg'] = bb.bollinger_mavg()
    data.loc[:, 'bollinger_pband'] = bb.bollinger_pband()
    data.loc[:, 'bollinger_wband'] = bb.bollinger_wband()

    return data



def add_volume_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Adds the volume indicators.

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
    chaikin = ChaikinMoneyFlowIndicator(data['high'], data['low'],
                                        data['close'], data['volume'])
    mfi = MFIIndicator(data['high'], data['low'], data['close'],
                       data['volume'])
    obv = OnBalanceVolumeIndicator(data['close'], data['volume'])

    data.loc[:, 'chaikin'] = chaikin.chaikin_money_flow()
    data.loc[:, 'mfi'] = mfi.money_flow_index()
    data.loc[:, 'obv'] = obv.on_balance_volume()

    return data
