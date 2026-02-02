"""
detectors.py

Order-flow detection logic:
- Bid/Ask imbalances (1:300)
- Stacked imbalances (3+)
- Unfinished business (failed auctions)
"""

IMBALANCE_RATIO = 300
STACKED_COUNT = 3


def detect_imbalances(bars):
    """
    Detect bid/ask imbalances per footprint bar.
    Returns list of:
    {
        bar: int,
        price: float,
        side: 'ASK' | 'BID'
    }
    """
    imbalances = []

    for bar_index, bar in enumerate(bars):
        for price, lvl in bar.levels.items():
            bid = lvl["bid"]
            ask = lvl["ask"]

            if bid > 0 and ask / bid >= IMBALANCE_RATIO:
                imbalances.append(
                    {"bar": bar_index, "price": price, "side": "ASK"}
                )

            elif ask > 0 and bid / ask >= IMBALANCE_RATIO:
                imbalances.append(
                    {"bar": bar_index, "price": price, "side": "BID"}
                )

    return imbalances


def detect_stacked_imbalances(imbalances):
    """
    Detect stacked imbalances (3+ consecutive price levels).
    Returns list of zones:
    {
        start_bar, end_bar, low, high, side
    }
    """
    zones = []
    if not imbalances:
        return zones

    imbalances = sorted(
        imbalances, key=lambda x: (x["bar"], x["side"], x["price"])
    )

    current = [imbalances[0]]

    for imb in imbalances[1:]:
        last = current[-1]

        if (
            imb["bar"] == last["bar"]
            and imb["side"] == last["side"]
            and abs(imb["price"] - last["price"]) < 1e-9
        ):
            current.append(imb)
        else:
            if len(current) >= STACKED_COUNT:
                prices = [x["price"] for x in current]
                zones.append(
                    {
                        "start_bar": current[0]["bar"],
                        "end_bar": current[-1]["bar"] + 1,
                        "low": min(prices),
                        "high": max(prices),
                        "side": current[0]["side"],
                    }
                )
            current = [imb]

    if len(current) >= STACKED_COUNT:
        prices = [x["price"] for x in current]
        zones.append(
            {
                "start_bar": current[0]["bar"],
                "end_bar": current[-1]["bar"] + 1,
                "low": min(prices),
                "high": max(prices),
                "side": current[0]["side"],
            }
        )

    return zones


def detect_unfinished_business(bars):
    """
    Detect unfinished auctions:
    - High with no bid
    - Low with no ask
    """
    unfinished = []

    for i, bar in enumerate(bars):
        if not bar.levels:
            continue

        prices = sorted(bar.levels.keys())
        low = prices[0]
        high = prices[-1]

        if bar.levels[high]["bid"] == 0:
            unfinished.append(
                {
                    "price": high,
                    "side": "ASK",
                    "start_bar": i,
                    "end_bar": i + 1,
                }
            )

        if bar.levels[low]["ask"] == 0:
            unfinished.append(
                {
                    "price": low,
                    "side": "BID",
                    "start_bar": i,
                    "end_bar": i + 1,
                }
            )

    return unfinished
