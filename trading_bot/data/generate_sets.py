import os

import pandas as pd

from trading_bot.indicators import add_indicators

# This folder
here = os.path.abspath(os.path.dirname(__file__))

# Read data
bitcoin = pd.read_csv(f'{here}/bitcoin.csv', parse_dates=['date'])

# Calculate indicators
bitcoin = add_indicators(bitcoin)

# Filter by date
mask = bitcoin['date'] >= pd.Timestamp('2018-03-01')
bitcoin = bitcoin.loc[mask]

# Keep last 30 days for testing
test_size = 30
test = bitcoin.iloc[-test_size:]
bitcoin = bitcoin.iloc[:-test_size]

# Split into train and validation
train_size = int(bitcoin.shape[0] * 0.8)
train = bitcoin.iloc[:train_size]
valid = bitcoin.iloc[train_size:]

# Export
test.to_csv(f'{here}/test.csv', index=False)
train.to_csv(f'{here}/train.csv', index=False)
valid.to_csv(f'{here}/valid.csv', index=False)

# Print sizes
print(f'Train size: {train.shape[0]}')
print(f'Validation size: {valid.shape[0]}')
print(f'Test size: {test.shape[0]}')
