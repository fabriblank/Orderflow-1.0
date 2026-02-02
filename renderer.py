"""
renderer.py

Responsible for rendering footprint (ladder) charts in Streamlit.
"""

import pandas as pd
import streamlit as st


def render_footprint(bars, imbalances=None, stacked=None, unfinished=None):
    """
    Render footprint ladder as a table.
    """

    if not bars:
        st.warning("No footprint data yet.")
        return

    rows = []

    for bar_index, bar in enumerate(bars):
        for price, lvl in sorted(bar.levels.items(), reverse=True):
            rows.append(
                {
                    "Bar": bar_index,
                    "Price": price,
                    "Bid": lvl["bid"],
                    "Ask": lvl["ask"],
                    "Delta": lvl["ask"] - lvl["bid"],
                    "Total": lvl["ask"] + lvl["bid"],
                }
            )

    df = pd.DataFrame(rows)

    st.subheader("📊 Footprint Ladder")
    st.dataframe(
        df,
        use_container_width=True,
        height=600,
    )

    # ---- Overlays ----
    if imbalances:
        st.subheader("⚡ Imbalances")
        st.json(imbalances)

    if stacked:
        st.subheader("🔥 Stacked Imbalances")
        st.json(stacked)

    if unfinished:
        st.subheader("❗ Unfinished Auctions")
        st.json(unfinished)
