""" app.py

Streamlit-safe True Footprint Ladder

Non-blocking (no while True)

Background Databento stream

Persistent engine state

Auto-refresh rendering """


import threading import time import streamlit as st

from config import SYMBOLS, BAR_SECONDS, MAX_BARS from data_stream import start_stream from footprint_engine import FootprintEngine from detectors import ( detect_imbalances, detect_stacked_imbalances, detect_unfinished_business, ) from renderer import render_footprint

--------------------------------------------------

Streamlit config

--------------------------------------------------

st.set_page_config(page_title="True Footprint Ladder", layout="wide") st.title("True Footprint Ladder")

--------------------------------------------------

Sidebar

--------------------------------------------------

st.sidebar.header("Settings") symbol = st.sidebar.selectbox("Instrument", SYMBOLS, index=0) show_table = st.sidebar.checkbox("Show CVD / Volume Table", value=True)

--------------------------------------------------

Session state

--------------------------------------------------

if "engine" not in st.session_state: st.session_state.engine = FootprintEngine(bar_seconds=BAR_SECONDS)

if "footprints" not in st.session_state: st.session_state.footprints = []

if "stream_running" not in st.session_state: st.session_state.stream_running = False

--------------------------------------------------

Background stream worker (SAFE)

--------------------------------------------------

def stream_worker(selected_symbol): for tick in start_stream(selected_symbol): bar = st.session_state.engine.process_tick(tick) if bar: st.session_state.footprints.append(bar) st.session_state.footprints = st.session_state.footprints[-MAX_BARS:]

--------------------------------------------------

Start stream once

--------------------------------------------------

if not st.session_state.stream_running: thread = threading.Thread( target=stream_worker, args=(symbol,), daemon=True, ) thread.start() st.session_state.stream_running = True

--------------------------------------------------

Detection pipeline

--------------------------------------------------

def run_detectors(bars): imbalances = detect_imbalances(bars) stacked = detect_stacked_imbalances(imbalances) unfinished = detect_unfinished_business(bars)

return {
    "imbalances": imbalances,
    "stacked_imbalances": stacked,
    "unfinished_business": unfinished,
}

--------------------------------------------------

Render (NO infinite loop)

--------------------------------------------------

if st.session_state.footprints: detections = run_detectors(st.session_state.footprints) fig = render_footprint( st.session_state.footprints, detections, show_table=show_table, ) st.plotly_chart(fig, use_container_width=True) else: st.info("Waiting for live futures data…")

--------------------------------------------------

Auto-refresh (Streamlit-safe heartbeat)

--------------------------------------------------

time.sleep(1) st.experimental_rerun()
