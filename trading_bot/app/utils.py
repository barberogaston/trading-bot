from operator import itemgetter
from typing import Dict


def get_action(probs: Dict[str, float]) -> str:
    probs = probs.copy()
    non_adjusted_action = max(probs.items(), key=itemgetter(1))[0]
    probs['SELL'] = probs['SELL'] * 0.98
    action = max(probs.items(), key=itemgetter(1))[0]
    if non_adjusted_action == 'SELL' and action == 'BUY':
        return 'HOLD'
    return action
