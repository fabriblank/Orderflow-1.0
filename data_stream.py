"""
data_stream.py

Databento live futures trade stream
Yields normalized tick data for the footprint engine
"""

import os
import databento as db


def start_stream(symbol: str):
    """
    Generator yielding normalized trade ticks:
    {
        price: float
        size: int
        side: 'BID' or 'ASK'
        ts: float (epoch seconds)
    }
    """

    api_key = os.environ.get("DATABENTO_API_KEY")
    if not api_key:
        raise RuntimeError("DATABENTO_API_KEY not set")

    client = db.Live(api_key)

    # CME Globex trades (centralized)
    client.subscribe(
        dataset="GLBX.MDP3",
        schema="trades",
        symbols=[symbol],
    )

    for msg in client:
        if msg.schema != "trades":
            continue

        yield {
            "price": float(msg.price),
            "size": int(msg.size),
            "side": "ASK" if msg.is_buyer_maker is False else "BID",
            "ts": msg.ts_event / 1_000_000_000,
    }
