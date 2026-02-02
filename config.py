config.py

Central configuration for Order Flow Footprint Platform

-----------------------------

ALLOWED CURRENCIES (STRICT)

-----------------------------

ALLOWED_CURRENCIES = { "EUR": "6E",  # Euro FX Futures "JPY": "6J",  # Japanese Yen Futures "AUD": "6A",  # Australian Dollar Futures }

Continuous front-month symbols (Databento format)

FUTURES_SYMBOLS = { "6E": "6E.c.0", "6J": "6J.c.0", "6A": "6A.c.0", }

-----------------------------

DATA SETTINGS

-----------------------------

DATASET = "GLBX.MDP3"      # CME Globex SCHEMA = "trades"          # Time & Sales

Footprint bar size (seconds)

FOOTPRINT_BAR_SECONDS = 60

-----------------------------

SESSION SETTINGS (CME)

-----------------------------

Times are in exchange time (CT). Adjust later if needed.

SESSIONS = { "RTH": { "start": "08:30", "end": "15:00", "reset_cvd": True, }, "ETH": { "start": "17:00", "end": "16:00", "reset_cvd": False, }, }

DEFAULT_SESSION = "RTH"

-----------------------------

IMBALANCE SETTINGS

-----------------------------

IMBALANCE_RATIO = 300           # 1 : 300 STACKED_IMBALANCE_MIN = 3       # consecutive levels IMBALANCE_TEXT_COLOR = "blue"  # always blue

-----------------------------

HVN SETTINGS

-----------------------------

HVN_PERCENTILE = 0.90            # top 10% volume per footprint HVN_OUTLINE_COLOR = "black" HVN_CONSECUTIVE_COLOR = "yellow"

-----------------------------

UNFINISHED BUSINESS SETTINGS

-----------------------------

UNFINISHED_LINE_OPACITY = 0.2 UNFINISHED_LINE_STYLE = "dashed"

-----------------------------

VISUAL SETTINGS

-----------------------------

DOMINANT_ASK_COLOR = (0, 200, 0)   # green DOMINANT_BID_COLOR = (200, 0, 0)   # red BACKGROUND_OPACITY_MIN = 0.1 BACKGROUND_OPACITY_MAX = 0.9

-----------------------------

TABLE SETTINGS

-----------------------------

SHOW_BOTTOM_TABLE_DEFAULT = True BOTTOM_TABLE_ROWS = 10

-----------------------------

VALIDATION

-----------------------------

def is_valid_symbol(symbol: str) -> bool: return symbol in FUTURES_SYMBOLS.values()
