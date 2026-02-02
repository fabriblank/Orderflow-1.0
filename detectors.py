detectors.py

Advanced order-flow detectors: imbalances, stacked imbalances, unfinished business

from typing import Dict, List, Tuple from config import ( IMBALANCE_RATIO, STACKED_IMBALANCE_MIN, )

class Imbalance: def init(self, price: float, side: str): self.price = price self.side = side  # 'ASK' or 'BID'

class StackedImbalanceZone: def init(self, prices: List[float], side: str): self.prices = prices self.side = side  # 'ASK' or 'BID' self.active = True

def contains(self, price: float) -> bool:
    return min(self.prices) <= price <= max(self.prices)

class UnfinishedBusiness: def init(self, price: float, side: str): self.price = price self.side = side  # 'ASK' for unfinished high, 'BID' for unfinished low self.active = True

-----------------------------

IMBALANCE DETECTION

-----------------------------

def detect_imbalances(levels: Dict[float, Dict[str, int]]) -> List[Imbalance]: imbalances = []

for price, vols in levels.items():
    bid = vols.get("bid", 0)
    ask = vols.get("ask", 0)

    if bid == 0 and ask == 0:
        continue

    # ask imbalance
    if bid > 0 and ask / bid >= IMBALANCE_RATIO:
        imbalances.append(Imbalance(price, "ASK"))

    # bid imbalance
    if ask > 0 and bid / ask >= IMBALANCE_RATIO:
        imbalances.append(Imbalance(price, "BID"))

return imbalances

-----------------------------

STACKED IMBALANCES

-----------------------------

def detect_stacked_imbalances(imbalances: List[Imbalance]) -> List[StackedImbalanceZone]: zones: List[StackedImbalanceZone] = []

if not imbalances:
    return zones

# group by side
by_side: Dict[str, List[float]] = {"ASK": [], "BID": []}
for imb in imbalances:
    by_side[imb.side].append(imb.price)

for side, prices in by_side.items():
    if len(prices) < STACKED_IMBALANCE_MIN:
        continue

    prices = sorted(prices)
    stack = [prices[0]]

    for p in prices[1:]:
        # consecutive price levels
        if abs(p - stack[-1]) <= 1e-9 or abs(p - stack[-1]) <= 0.25:
            stack.append(p)
        else:
            if len(stack) >= STACKED_IMBALANCE_MIN:
                zones.append(StackedImbalanceZone(stack.copy(), side))
            stack = [p]

    if len(stack) >= STACKED_IMBALANCE_MIN:
        zones.append(StackedImbalanceZone(stack.copy(), side))

return zones

-----------------------------

UNFINISHED BUSINESS (FAILED AUCTION)

-----------------------------

def detect_unfinished_business(levels: Dict[float, Dict[str, int]]) -> List[UnfinishedBusiness]: results: List[UnfinishedBusiness] = []

if not levels:
    return results

prices = sorted(levels.keys())
low = prices[-1]
high = prices[0]

low_vols = levels[low]
high_vols = levels[high]

# unfinished low: only bid traded
if low_vols.get("ask", 0) == 0 and low_vols.get("bid", 0) > 0:
    results.append(UnfinishedBusiness(low, "BID"))

# unfinished high: only ask traded
if high_vols.get("bid", 0) == 0 and high_vols.get("ask", 0) > 0:
    results.append(UnfinishedBusiness(high, "ASK"))

return results
