footprint_engine.py

Core footprint aggregation engine (tick -> footprint bars)

from collections import defaultdict from typing import Dict, List from config import FOOTPRINT_BAR_SECONDS, HVN_PERCENTILE

class FootprintBar: def init(self, start_ts: int): self.start_ts = start_ts # price -> {bid, ask} self.levels: Dict[float, Dict[str, int]] = defaultdict(lambda: {"bid": 0, "ask": 0}) self.bar_delta = 0 self.total_volume = 0 self.hvn_prices: List[float] = []

def add_trade(self, price: float, size: int, side: str):
    if side == "BUY":
        self.levels[price]["ask"] += size
        self.bar_delta += size
    else:
        self.levels[price]["bid"] += size
        self.bar_delta -= size
    self.total_volume += size

def finalize(self):
    # Detect HVNs using percentile of total volume per price
    volumes = []
    for vols in self.levels.values():
        volumes.append(vols["bid"] + vols["ask"])

    if not volumes:
        return

    volumes_sorted = sorted(volumes)
    idx = int(len(volumes_sorted) * HVN_PERCENTILE)
    threshold = volumes_sorted[min(idx, len(volumes_sorted) - 1)]

    self.hvn_prices = [
        price for price, vols in self.levels.items()
        if (vols["bid"] + vols["ask"]) >= threshold
    ]

class FootprintEngine: def init(self): self.current_bar: FootprintBar | None = None self.completed_bars: List[FootprintBar] = [] self.cvd = 0

def ingest_trade(self, timestamp: int, price: float, size: int, side: str):
    if self.current_bar is None:
        self.current_bar = FootprintBar(start_ts=timestamp)

    # roll bar
    if timestamp - self.current_bar.start_ts >= FOOTPRINT_BAR_SECONDS:
        self._close_current_bar()
        self.current_bar = FootprintBar(start_ts=timestamp)

    self.current_bar.add_trade(price, size, side)

def _close_current_bar(self):
    if not self.current_bar:
        return

    self.current_bar.finalize()
    self.cvd += self.current_bar.bar_delta
    self.completed_bars.append(self.current_bar)

def get_last_bar(self) -> FootprintBar | None:
    return self.completed_bars[-1] if self.completed_bars else None
