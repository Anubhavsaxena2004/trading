import asyncio, websockets, json, time
from collections import deque
from tasks import notify_threshold
import requests
from datetime import datetime

PRICE_HISTORY = {}  # {ticker: deque(maxlen=60)}
AVG_PRICES = {}  # {ticker: [prices]}
LAST_AVG_CALC = {}  # {ticker: timestamp}

async def monitor_prices():
    async with websockets.connect("ws://localhost:8765") as ws:
        while True:
            data = json.loads(await ws.recv())
            ticker, price = data["ticker"], data["price"]
            
            # Track last 60 seconds of prices
            if ticker not in PRICE_HISTORY:
                PRICE_HISTORY[ticker] = deque(maxlen=60)
                AVG_PRICES[ticker] = []
                LAST_AVG_CALC[ticker] = time.time()
            
            PRICE_HISTORY[ticker].append(price)
            AVG_PRICES[ticker].append(price)
            
            # Check 2% increase in 1 minute
            if len(PRICE_HISTORY[ticker]) == 60:
                old_price = PRICE_HISTORY[ticker][0]
                if price > old_price * 1.02:
                    notify_threshold.delay(ticker, price)
            
            # Calculate average price every 5 minutes
            current_time = time.time()
            if current_time - LAST_AVG_CALC[ticker] >= 300:  # 5 minutes = 300 seconds
                avg_price = sum(AVG_PRICES[ticker]) / len(AVG_PRICES[ticker])
                
                # Store in database via API
                requests.post(
                    "http://localhost:8000/api/avg-prices",
                    json={
                        "ticker": ticker,
                        "avg_price": avg_price,
                        "timestamp": datetime.now().isoformat()
                    }
                )
                
                # Reset for next period
                AVG_PRICES[ticker] = []
                LAST_AVG_CALC[ticker] = current_time

asyncio.run(monitor_prices())