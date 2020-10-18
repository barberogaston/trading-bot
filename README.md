# Overview

This project implements a Stock Trading Bot, trained using Deep Reinforcement Learning, specifically Deep Q-learning. Implementation is kept simple and as close as possible to the algorithm discussed in the paper, for learning purposes.

## Introduction

Generally, Reinforcement Learning is a family of machine learning techniques that allow us to create intelligent agents that learn from the environment by interacting with it, as they learn an optimal policy by trial and error. This is especially useful in many real world tasks where supervised learning might not be the best approach due to various reasons like nature of task itself, lack of appropriate labelled data, etc.

The important idea here is that this technique can be applied to any real world task that can be described loosely as a Markovian process.

## Approach

This work uses a Model-free Reinforcement Learning technique called Deep Q-Learning (neural variant of Q-Learning).
At any given time (episode), an agent abserves it's current state (n-day window stock price representation), selects and performs an action (buy/sell/hold), observes a subsequent state, receives some reward signal (difference in portfolio position) and lastly adjusts it's parameters based on the gradient of the loss computed.

There have been several improvements to the Q-learning algorithm over the years, and a few have been implemented in this project:

- [x] Vanilla DQN
- [x] DQN with fixed target distribution
- [x] Double DQN
- [ ] Prioritized Experience Replay
- [ ] Dueling Network Architectures

## Some Caveats

- At any given state, the agent can only decide to buy/sell if and only if it has performed the opposite operation before, being this only true after the first buy. In other words, the agent can't sell if it hasn't bought anything and the same way around.
- The n-day window feature representation is a vector of subsequent differences in Adjusted Closing price of the stock we're trading followed by a sigmoid operation, done in order to normalize the values to the range [0, 1].
- Training is prefferably done on CPU due to it's sequential manner, after each episode of trading we replay the experience (1 epoch over a small minibatch) and update model parameters.

## Data

Download bitcoin's historical data with the following command.

```bash
python trading_bot/data/download.py
```

This will download data from bitcoin's start up to yesterday, meaning new data will be available after 00:00 UTC.

## Getting Started

### Install dependencies

In order to use this project, you'll need to install the required python packages:

```bash
pip install -e .
```

### Training and validating

Now you can open up a terminal and start training the agent:

```bash
cd trading_bot
python train.py data/train.csv data/valid.csv --strategy t-dqn --window-size=10
```

### Testing with unseen data

Once you're done training, run the evaluation script and let the agent make trading decisions:

```bash
python eval.py data/test.csv --model-name model --debug
```

### Serving predictions

Once you have trained, validated and tested your model, you can obtain predictions each day at 00:05 UTC (leave a 5 minute margin for the API to load yesterday's data).

The following execution creates a Docker container and starts a local API to which you can request which action to take based on yesterda's state.

```bash
python app.py --model-name=model

# In case you want ot rebuild the container add the --rebuild flag
python app.py --model-name=model --rebuild
```

### GET action

**URL:** `http://localhost:8000/action` <br>
**Method:** `GET` <br>
**Response**

```json
{
    "action": "SELL", // BUY, SELL or HOLD
    "close": 11358.10156733,
    "date": "2020-10-17",
    "probs": {
        "BUY": 0.405701607465744,
        "HOLD": 0.3922637701034546,
        "SELL": 0.4192860424518585
    }
}
```

## Acknowledgements

- [@keon](https://github.com/keon) for [deep-q-learning](https://github.com/keon/deep-q-learning)
- [@edwardhdlu](https://github.com/edwardhdlu) for [q-trader](https://github.com/edwardhdlu/q-trader)
- [Prabhsimran Singh](https://github.com/pskrunner14) for providing the [original repo](https://github.com/pskrunner14/trading-bot)

## References

- [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602)
- [Human Level Control Through Deep Reinforcement Learning](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/)
- [Deep Reinforcement Learning with Double Q-Learning](https://arxiv.org/abs/1509.06461)
- [Prioritized Experience Replay](https://arxiv.org/abs/1511.05952)
- [Dueling Network Architectures for Deep Reinforcement Learning](https://arxiv.org/abs/1511.06581)