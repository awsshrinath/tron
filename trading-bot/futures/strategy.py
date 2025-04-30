import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from execution import get_market_data
from volume_helper import is_volume_strong
from nifty_filter import get_nifty_trend
from global_signals import get_global_sentiment
from oi_helper import get_oi_trend  # Simulated for now

opening_range_high = {}
opening_range_low = {}

def breakout_strategy(symbol, capital):
    now = datetime.now().strftime('%H:%M')

    # Only consider trades after 9:45
    if now < "09:45":
        print(f"⏱️ Skipping {symbol}: Waiting till 9:45")
        return None

    price, high, low = get_market_data(symbol)

    # Store first candle range (simulate opening range)
    if symbol not in opening_range_high:
        opening_range_high[symbol] = high
        opening_range_low[symbol] = low

    or_high = opening_range_high[symbol]
    or_low = opening_range_low[symbol]

    # Breakout condition
    if price <= or_high:
        print(f"📉 Skipping {symbol}: No breakout yet")
        return None

    # Volume filter
    if not is_volume_strong(symbol):
        print(f"🔇 Skipping {symbol}: Weak volume")
        return None

    # Nifty/BankNifty alignment
    if get_nifty_trend() != "UP":
        print(f"📉 Skipping {symbol}: Nifty not trending up")
        return None

    # Simulated OI check
    oi_trend = get_oi_trend(symbol)
    if oi_trend != "LONG":
        print(f"📉 Skipping {symbol}: OI trend is {oi_trend}")
        return None

    # Global sentiment
    global_sentiment = get_global_sentiment()
    if not global_sentiment["allow_trading"]:
        print(f"🌍 Skipping {symbol}: {global_sentiment.get('reason', 'Global filter failed')}")
        return None

    # ✅ All filters passed
    print(f"✅ {symbol} breakout confirmed with strong volume and trend")

    return {
        "entry": price,
        "reason": "Breakout + Volume + OI + Global Confirmation"
    }
