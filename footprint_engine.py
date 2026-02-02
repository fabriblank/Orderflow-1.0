"""
footprint_engine.py

Builds footprint bars from trade ticks
"""

from collections import defaultdict
import math
import time


class FootprintBar:
    def __init__(self, start_ts, tick_size):
        self.start_ts = start_ts
        self.tick_size = tick_size
        self.levels = defaultdict(lambda: {"bid": 0, "ask": 0})
        self.delta = 0
        self.volume = 0


class FootprintEngine:
    def __init__(self, bar_seconds=60, tick_size=0.0001):
        self.bar_seconds = bar_seconds
        self.tick_size = tick_size
        self.current_bar = None

    def _price_to_level(self, price: float) -> float:
        return round(price / self.tick_size) * self.tick_size

    def process_tick(self, tick: dict):
        """
        tick = {
            price: float
            size: int
            side: 'BID' | 'ASK'
            ts: float
        }
        """

        ts = tick["ts"]

        if self.current_bar is None:
            self.current_bar = FootprintBar(ts, self.tick_size)

        # Bar rollover
        if ts - self.current_bar.start_ts >= self.bar_seconds:
            finished = self.current_bar
            self.current_bar = FootprintBar(ts, self.tick_size)
            return finished

        price_level = self._price_to_level(tick["price"])
        size = tick["size"]

        if tick["side"] == "ASK":
            self.current_bar.levels[price_level]["ask"] += size
            self.current_bar.delta += size
        else:
            self.current_bar.levels[price_level]["bid"] += size
            self.current_bar.delta -= size

        self.current_bar.volume += size
        return None
