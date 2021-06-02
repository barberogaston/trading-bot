from operator import itemgetter
from typing import Dict


def get_action(probs: Dict[str, float]) -> str:
    probs = probs.copy()
    return max(probs.items(), key=itemgetter(1))[0]
