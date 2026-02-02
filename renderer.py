""" renderer.py

Rendering engine for true footprint ladder. Uses Plotly for browser-based rendering (Streamlit-compatible). Pure rendering only – no detection logic here. """

import plotly.graph_objects as go

-----------------------------

Color utilities

-----------------------------

def volume_opacity(volume, max_volume): if max_volume == 0: return 0.1 return max(0.1, min(1.0, volume / max_volume))

-----------------------------

Footprint renderer

-----------------------------

def render_footprint(footprints, detections, show_table=True): """ footprints: list of footprint bars from FootprintEngine detections: output from detectors.py """

fig = go.Figure()

x_index = list(range(len(footprints)))

for i, bar in enumerate(footprints):
    max_vol = max(
        [(lvl['bid'] + lvl['ask']) for lvl in bar.levels.values()] or [1]
    )

    for price, lvl in bar.levels.items():
        bid = lvl['bid']
        ask = lvl['ask']
        total = bid + ask

        # Cell color logic
        if ask > bid:
            color = 'rgba(0,200,0,{})'.format(volume_opacity(total, max_vol))
        else:
            color = 'rgba(200,0,0,{})'.format(volume_opacity(total, max_vol))

        fig.add_shape(
            type='rect',
            x0=i - 0.45,
            x1=i + 0.45,
            y0=price - bar.tick_size / 2,
            y1=price + bar.tick_size / 2,
            fillcolor=color,
            line=dict(width=0)
        )

        # Bid / Ask text
        fig.add_annotation(
            x=i,
            y=price,
            text=f"{bid} | {ask}",
            showarrow=False,
            font=dict(size=9, color='white')
        )

    # Delta below bar
    delta_color = 'green' if bar.delta > 0 else 'red'
    fig.add_annotation(
        x=i,
        y=min(bar.levels.keys()) - bar.tick_size * 2,
        text=str(bar.delta),
        showarrow=False,
        font=dict(size=10, color=delta_color)
    )

# -----------------------------
# Imbalances (blue text)
# -----------------------------
for imb in detections.get('imbalances', []):
    fig.add_annotation(
        x=imb['bar'],
        y=imb['price'],
        text='IMB',
        showarrow=False,
        font=dict(color='blue', size=8)
    )

# -----------------------------
# Stacked imbalance zones
# -----------------------------
for zone in detections.get('stacked_imbalances', []):
    fig.add_shape(
        type='rect',
        x0=zone['start_bar'],
        x1=zone['end_bar'],
        y0=zone['low'],
        y1=zone['high'],
        fillcolor='rgba(0,255,0,0.15)' if zone['side'] == 'ASK' else 'rgba(255,0,0,0.15)',
        line=dict(width=0),
        layer='below'
    )

# -----------------------------
# Unfinished business lines
# -----------------------------
for ub in detections.get('unfinished_business', []):
    fig.add_shape(
        type='line',
        x0=ub['start_bar'],
        x1=ub['end_bar'],
        y0=ub['price'],
        y1=ub['price'],
        line=dict(
            color='rgba(0,255,0,0.3)' if ub['side'] == 'ASK' else 'rgba(255,0,0,0.3)',
            dash='dot'
        ),
        layer='below'
    )

# -----------------------------
# Layout
# -----------------------------
fig.update_layout(
    template='plotly_dark',
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
    height=800,
    margin=dict(l=40, r=40, t=40, b=40)
)

return fig
