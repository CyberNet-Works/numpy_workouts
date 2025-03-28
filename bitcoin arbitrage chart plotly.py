import pandas as pd
import plotly.graph_objs as go

# Load your BTC log
df = pd.read_csv("btc_price_log.csv")

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter only price columns (exclude _change, _pct)
price_columns = [col for col in df.columns if col.endswith('_price') and 'AVG' not in col]
avg_column = 'AVG_price'

# Create traces for each exchange
traces = []
for col in price_columns:
    traces.append(go.Scatter(
        x=df['timestamp'],
        y=df[col],
        mode='lines+markers',
        name=col.replace('_price', '')
    ))

# Add average price as its own line
if avg_column in df.columns:
    traces.append(go.Scatter(
        x=df['timestamp'],
        y=df[avg_column],
        mode='lines',
        name='Average',
        line=dict(dash='dash', width=2, color='black')
    ))

# Create layout
layout = go.Layout(
    title="BTC Spot Price by Exchange",
    xaxis=dict(title='Time'),
    yaxis=dict(title='Price (USD)'),
    legend=dict(x=0, y=1),
    hovermode='x unified'
)

# Build figure
fig = go.Figure(data=traces, layout=layout)

# Show interactive chart
fig.show()
