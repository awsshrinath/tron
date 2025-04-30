import sys
import os
from datetime import datetime
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from volume_helper import is_volume_strong
from execution import get_market_data
from nifty_filter import get_nifty_trend
from strategy import breakout_strategy  # Placeholder for your actual futures strategy

# CONFIG
FUTURE_SYMBOL = "NIFTY24APRFUT"
CAPITAL = 100000
TRADE_LOG = "futures_paper_log.csv"
ENTRY_TIME = "09:30"
EXIT_TIME = "15:18"

position = None

def log_trade(symbol, entry_price, exit_price, result, reason):
    pnl = round((exit_price - entry_price), 2) if result != "SKIPPED" else 0
    with open(TRADE_LOG, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{symbol},{entry_price},{exit_price},{result},{pnl},{reason}\n")

print("📊 Futures Paper Bot started...")

try:
    while True:
        now = datetime.now().strftime('%H:%M')

        if now < ENTRY_TIME:
            time.sleep(10)
            continue

        if now >= EXIT_TIME:
            if position:
                exit_price, _, _ = get_market_data(FUTURE_SYMBOL)
                print(f"⏰ Auto exit at {EXIT_TIME} for {FUTURE_SYMBOL} at ₹{exit_price}")
                log_trade(FUTURE_SYMBOL, position["entry"], exit_price, "AUTO-EXIT", position["reason"])
                position = None
            print("✅ Market close. Paper bot stopped.")
            break

        if not position:
            # Global filter: Nifty trend
            trend = get_nifty_trend()
            if trend != "UP":
                print(f"⚠️ Skipping entry: Nifty trend is {trend}")
                time.sleep(60)
                continue

            # Volume filter
            if not is_volume_strong(FUTURE_SYMBOL):
                print(f"⚠️ Skipping entry: Weak volume for {FUTURE_SYMBOL}")
                time.sleep(60)
                continue

            # Strategy
            signal = breakout_strategy(FUTURE_SYMBOL, CAPITAL)
            if signal:
                position = {
                    "entry": signal["entry"],
                    "reason": signal["reason"]
                }
                print(f"✅ Simulated ENTRY: {FUTURE_SYMBOL} at ₹{signal['entry']} [{signal['reason']}]")
                log_trade(FUTURE_SYMBOL, signal["entry"], "-", "OPEN", signal["reason"])

        else:
            # Monitor for manual exit (optional logic for SL/target simulation)
            price, _, _ = get_market_data(FUTURE_SYMBOL)
            print(f"📈 Holding {FUTURE_SYMBOL} | Current Price: ₹{price}")
            time.sleep(60)

except Exception as e:
    print(f"❌ Paper bot crashed: {e}")
