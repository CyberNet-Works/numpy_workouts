import requests
import time
import csv
from datetime import datetime

import os
print("📁 Saving log to:", os.path.abspath("btc_price_log.csv"))

# ANSI color codes
RESET = "\033[0m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREY = "\033[37m"
GREEN = "\033[92m"

# Unicode arrows
UP = "↑"
DOWN = "↓"
STABLE = "→"

# CSV log file
LOG_FILE = "btc_price_log.csv"
REFRESH_INTERVAL = 30  # seconds

# Track previous prices
previous_prices = {}

# Exchange APIs and JSON paths
SOURCES = {
    'Binance': ("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", ['price']),
    'Coinbase': ("https://api.coinbase.com/v2/prices/BTC-USD/spot", ['data', 'amount']),
    'Kraken': ("https://api.kraken.com/0/public/Ticker?pair=XBTUSD", ['result', 'XXBTZUSD', 'c', 0]),
    'Bitstamp': ("https://www.bitstamp.net/api/v2/ticker/btcusd/", ['last']),
    'Bitfinex': ("https://api.bitfinex.com/v1/pubticker/btcusd", ['last_price']),
    'Bybit': ("https://api.bybit.com/v2/public/tickers?symbol=BTCUSD", ['result', 0, 'last_price']),
    'OKX': ("https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT", ['data', 0, 'last']),
    'KuCoin': ("https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT", ['data', 'price'])
}

def get_price(url, path):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        for p in path:
            data = data[p]
        return float(data)
    except:
        return None

# Initialize CSV
with open(LOG_FILE, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['timestamp'] +
        [f"{name}_price" for name in SOURCES.keys()] +
        [f"{name}_change" for name in SOURCES.keys()] +
        [f"{name}_pct" for name in SOURCES.keys()] +
        ['AVG_price', 'AVG_change', 'AVG_pct']
    )

print("🔁 Starting BTC price monitoring...\nPress Ctrl+C to stop.\n")

try:
    while True:
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        prices = {}

        for name, (url, path) in SOURCES.items():
            prices[name] = get_price(url, path)

        valid_prices = {k: v for k, v in prices.items() if v is not None}
        if not valid_prices:
            print("❌ All requests failed.")
            time.sleep(REFRESH_INTERVAL)
            continue

        low = min(valid_prices.values())
        high = max(valid_prices.values())
        sorted_prices = sorted(valid_prices.items(), key=lambda x: x[1], reverse=True)

        print(f"\n🕒 {timestamp} UTC")
        for name, price in sorted_prices:
            color = YELLOW if price == high else RED if price == low else GREY

            prev = previous_prices.get(name)
            if prev is not None:
                delta = price - prev
                pct = (delta / prev) * 100 if prev != 0 else 0
                if delta > 0:
                    arrow = UP
                    delta_color = GREEN
                elif delta < 0:
                    arrow = DOWN
                    delta_color = RED
                else:
                    arrow = STABLE
                    delta_color = GREY
                change_str = f"{delta_color} {arrow} ${delta:.2f} ({pct:.2f}%){RESET}"
            else:
                change_str = f"{GREY} {STABLE} --- (--%) {RESET}"

            print(f"{color}{name:10s}: ${price:.2f} {change_str}{RESET}")
            previous_prices[name] = price

        spread = high - low
        print(f"\n📉 Spread: ${spread:.2f}")

        # Average price & change
        avg_price = sum(valid_prices.values()) / len(valid_prices)
        prev_avg = previous_prices.get("AVG")
        if prev_avg is not None:
            delta_avg = avg_price - prev_avg
            pct_avg = (delta_avg / prev_avg) * 100 if prev_avg != 0 else 0
            if delta_avg > 0:
                arrow = UP
                color = GREEN
            elif delta_avg < 0:
                arrow = DOWN
                color = RED
            else:
                arrow = STABLE
                color = GREY
            print(f"\n📊 {color}Avg Price: ${avg_price:.2f} {arrow} ${delta_avg:.2f} ({pct_avg:.2f}%){RESET}")
        else:
            delta_avg = pct_avg = None
            print(f"\n📊 Avg Price: ${avg_price:.2f}")

        previous_prices["AVG"] = avg_price

        # Log to CSV
        with open(LOG_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            row = [timestamp]
            for name in SOURCES.keys():
                row.append(prices.get(name))
            for name in SOURCES.keys():
                prev = previous_prices.get(name)
                curr = prices.get(name)
                if curr is not None and prev is not None:
                    row.append(curr - prev)
                else:
                    row.append(None)
            for name in SOURCES.keys():
                prev = previous_prices.get(name)
                curr = prices.get(name)
                if curr is not None and prev and prev != 0:
                    row.append((curr - prev) / prev * 100)
                else:
                    row.append(None)
            row.extend([avg_price, delta_avg, pct_avg])
            writer.writerow(row)

        time.sleep(REFRESH_INTERVAL)

except KeyboardInterrupt:
    print("\n⏹ Monitoring stopped.")
