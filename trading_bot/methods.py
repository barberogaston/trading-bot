import logging

import numpy as np

from tqdm import tqdm

from trading_bot.utils import (
    format_currency,
    format_position
)
from trading_bot.ops import (
    get_state
)


def train_model(agent, episode, data, ep_count=100, batch_size=32,
                window_size=10):
    total_profit = 0
    data_length = data.shape[0] - 1

    agent.inventory = []
    avg_loss = []

    state = get_state(data, 0, window_size + 1)

    for t in tqdm(range(data_length), total=data_length, leave=True,
                  desc='Episode {}/{}'.format(episode, ep_count)):
        reward = 0
        next_state = get_state(data, t + 1, window_size + 1)

        # select an action
        action = agent.act(state)

        # BUY
        if action == 1 and len(agent.inventory) == 0:
            agent.inventory.append(close)

        # SELL
        elif (
            action == 2 and len(agent.inventory) > 0 and
            agent.inventory[0] < close
        ):
            reward = 0
            for item in agent.inventory:
              delta = close - item
              reward += delta  # max(delta, 0)
            total_profit += reward
            agent.inventory = []

        # HOLD
        else:
            pass

        done = (t == data_length - 1)
        agent.remember(state, action, reward, next_state, done)

        if len(agent.memory) > batch_size:
            loss = agent.train_experience_replay(batch_size)
            avg_loss.append(loss)

        state = next_state

    agent.save(episode)

    return (episode, ep_count, total_profit, np.mean(np.array(avg_loss)))


def evaluate_model(agent, data, window_size, debug):
    total_profit = 0
    data_length = data.shape[0] - 1

    history = []
    agent.inventory = []

    state = get_state(data, 0, window_size + 1)

    for t in range(data_length):
        reward = 0
        next_state = get_state(data, t + 1, window_size + 1)

        # select an action
        action = agent.act(state, is_eval=True)
        close = data.iloc[t].loc['close']

        # BUY
        if action == 1 and len(agent.inventory) == 0:
            agent.inventory.append(close)

            history.append((close, "BUY"))
            if debug:
                logging.debug("Buy at: {}".format(
                    format_currency(close)))

        # SELL
        elif (
            action == 2 and len(agent.inventory) > 0
            and agent.inventory[0] < close
        ):
            reward = 0
            for item in agent.inventory:
                delta = close - item
                if debug:
                    logging.debug("Sell at: {} | Position: {}".format(
                        format_currency(close),
                        format_position(close - item)))
                reward += delta  # max(delta, 0)
            total_profit += reward
            agent.inventory = []

            history.append((close, "SELL"))
            with open('eval_log.csv', 'a+') as f:
                f.write(f'{close},BUY\n')
        # HOLD
        else:
            history.append((close, "HOLD"))

        done = (t == data_length - 1)
        agent.memory.append((state, action, reward, next_state, done))

        state = next_state
        if done:
            return total_profit, history
