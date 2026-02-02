data_stream.py

Databento live data streaming for centralized currency futures

import threading import databento as db from datetime import datetime from config import DATASET, SCHEMA, FUTURES_SYMBOLS from state import RuntimeState

class DataStreamer: def init(self, api_key: str, symbol_key: str, state: RuntimeState): """ symbol_key: one of '6E', '6J', '6A' state: shared RuntimeState instance """ if symbol_key not in FUTURES_SYMBOLS: raise ValueError(f"Unsupported symbol {symbol_key}")

self.symbol = FUTURES_SYMBOLS[symbol_key]
    self.state = state
    self.client = db.Live(key=api_key)
    self._thread = None
    self._running = False

def start(self):
    if self._running:
        return
    self._running = True
    self._thread = threading.Thread(target=self._run, daemon=True)
    self._thread.start()

def stop(self):
    self._running = False

def _run(self):
    self.client.subscribe(
        dataset=DATASET,
        schema=SCHEMA,
        symbols=[self.symbol],
    )

    for msg in self.client:
        if not self._running:
            break

        # Only process trade messages
        try:
            ts = msg.ts_event
            price = msg.price
            size = msg.size
            side = msg.side  # BUY or SELL
        except AttributeError:
            continue

        # Normalize timestamp to seconds
        ts_sec = ts // 1_000_000_000

        self.state.ingest_trade(
            timestamp=ts_sec,
            price=price,
            size=size,
            side=side,
        )

def is_running(self) -> bool:
    return self._running
