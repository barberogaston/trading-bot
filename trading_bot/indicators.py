from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD, SMAIndicator


def add_indicators(data):
    rsi = RSIIndicator(data['close'])
    ema = EMAIndicator(data['close'])
    sma = SMAIndicator(data['close'], n=14)
    macd = MACD(data['close'])

    data.loc[:, 'rsi'] = rsi.rsi()
    data.loc[:, 'ema'] = ema.ema_indicator()
    data.loc[:, 'sma'] = sma.sma_indicator()
    data.loc[:, 'macd'] = macd.macd()
    data.loc[:, 'macd_diff'] = macd.macd_diff()
    data.loc[:, 'macd_signal'] = macd.macd_signal()

    return data
