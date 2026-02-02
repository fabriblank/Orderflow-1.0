""" app.py

Main application entry point.

Streams CME futures data via Databento

Builds footprint bars

Runs order-flow detectors

Renders true footprint ladder


Designed to run continuously on server (Streamlit / cloud VM) """

import threading import time import streamlit as st

from config import SYMBOLS, BAR_SECONDS, MAX_BARS from data_stream import start_stream from footprint_engine import FootprintEngine from detectors import ( detect_imbalances, detect_stacked_imbalances, detect_unfinished_business ) from renderer import render_footprint

-----------------------------

Streamlit setup

-----------------------------

st.set_page_config(layout="wide", page_title="True Footprint Ladder") st.title("True Footprint Ladder")

Sidebar controls

st.sidebar.header("Settings") show_table = st.sidebar.checkbox("Show CVD / Volume Table", value=True)

symbol = st.sidebar.selectbox( "Instrument", SYMBOLS, index=0 )

-----------------------------

State initialization

-----------------------------

if "engine" not in st.session_state: st.session_state.engine = FootprintEngine(bar_seconds=BAR_SECONDS)

if "footprints" not in st.session_state: st.session_state.footprints = []

if "running" not in st.session_state: st.session_state.running = False

-----------------------------

Data stream thread

-----------------------------

def stream_worker(): for tick in start_stream(symbol): bar = st.session_state.engine.process_tick(tick) if bar: st.session_state.footprints.append(bar) st.session_state.footprints = st.session_state.footprints[-MAX_BARS:]

-----------------------------

Start stream once

-----------------------------

if not st.session_state.running: thread = threading.Thread(target=stream_worker, daemon=True) thread.start() st.session_state.running = True

-----------------------------

Detection pipeline

-----------------------------

def run_detectors(bars): imbalances = detect_imbalances(bars) stacked = detect_stacked_imbalances(imbalances) unfinished = detect_unfinished_business(bars)

return {
    "imbalances": imbalances,
    "stacked_imbalances": stacked,
    "unfinished_business": unfinished
}

-----------------------------

Main render loop

-----------------------------

placeholder = st.empty()

while True: if st.session_state.footprints: detections = run_detectors(st.session_state.footprints) fig = render_footprint( st.session_state.footprints, detections, show_table=show_table ) placeholder.plotly_chart(fig, use_container_width=True)

time.sleep(1)
