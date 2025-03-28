import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import time

CSV_FILE = "btc_price_log.csv"
REFRESH_INTERVAL = 30  # seconds

st.set_page_config(page_title="BTC Price Monitor", layout="wide")

st.title("📊 BTC Spot Price by Exchange (Live Chart)")
st.caption(f"Auto-refreshes every {REFRESH_INTERVAL} seconds. Data source: btc_price_log.csv")

# Main loop
def load_data():
    if not os.path.exists(CSV_FILE):
        st.warning("btc_price_log.csv not found. Run your monitor script first.")
        return pd.DataFrame()
    
    df = pd.read_csv(CSV_FILE)
    if df.empty or 'timestamp' not in df.columns:
        st.warning("Waiting for data...")
        return pd.DataFrame()
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def plot_prices(df):
    price_columns = [col for col in df.columns if col.endswith('_price') and 'AVG' not in col]
    avg_column = 'AVG_price'

    traces = []
    for col in price_columns:
        traces.append(go.Scatter(
            x=df['timestamp'],
            y=df[col],
            mode='lines+markers',
            name=col.replace('_price', '')
        ))

    if avg_column in df.columns:
        traces.append(go.Scatter(
            x=df['timestamp'],
            y=df[avg_column],
            mode='lines',
            name='Average',
            line=dict(dash='dash', width=2, color='black')
        ))

    layout = go.Layout(
        xaxis=dict(title='Time'),
        yaxis=dict(title='Price (USD)'),
        hovermode='x unified',
        legend=dict(x=0, y=1)
    )

    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig, use_container_width=True)

# Streamlit loop
placeholder = st.empty()

while True:
    df = load_data()
    if not df.empty:
        with placeholder.container():
            plot_prices(df)
    time.sleep(REFRESH_INTERVAL)
