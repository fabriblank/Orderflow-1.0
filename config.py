"""
config.py

Global configuration for the footprint platform
Centralized futures only
"""

# --------------------------------------------------
# Supported instruments (centralized futures)
# --------------------------------------------------

SYMBOLS = [
    "6A",  # AUD futures
    "6B",  # GBP futures
    "6C",  # CAD futures
    "6E",  # EUR futures
    "6J",  # JPY futures
]

# --------------------------------------------------
# Footprint settings
# --------------------------------------------------

BAR_SECONDS = 60        # 1-minute footprint bars
MAX_BARS = 100          # Rolling bars kept in memory

# --------------------------------------------------
# Databento dataset (CME)
# --------------------------------------------------

DATABENTO_DATASET = "GLBX.MDP3"
