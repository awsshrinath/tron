import time
from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scalp_strategy import scalper_strategy
from log_helper import log_entry, log_exit
from utils import kite

INDICES = ["NIFTY", "BANKNIFTY"]
CAPITAL = 10000
TRADE_LIMIT = 2
DAILY_TARGET = 100
DAILY_STOPLOSS = 60

trade_count = 0
total_pnl = 0
active_trades = {}

print("\n📈 Option Scalper Paper Bot Started...")

try:
    while True:
        now = datetime.now().strftime("%H:%M")
        if now >= "15:00":
            print("🔔 3:00 PM reached. No new trades allowed.")
            break

        if trade_count >= TRADE_LIMIT:
            print("🛑 Max trades reached for the day.")
            break

        if total_pnl <= -DAILY_STOPLOSS:
            print("🔻 Daily loss limit hit.")
            break

        if total_pnl >= DAILY_TARGET:
            print("🟢 Daily profit target achieved.")
            break

        for index in INDICES:
            if index in active_trades:
                continue

            trade = scalper_strategy(index, CAPITAL)
            if trade:
                trade_count += 1
                active_trades[index] = trade

                log_entry(
                    index,
                    trade["option_symbol"],
                    trade["entry_price"],
                    trade["sl"],
                    trade["target"],
                    trade["direction"],
                    trade["reason"]
                )

        for index, trade in list(active_trades.items()):
            option_symbol = trade["option_symbol"]
            time.sleep(0.4)
            try:
                ltp = kite.ltp(option_symbol)[option_symbol]["last_price"]
            except Exception as e:
                print(f"❌ Error fetching LTP for {option_symbol}: {e}")
                continue

            if ltp >= trade["target"]:
                pnl = ltp - trade["entry_price"]
                print(f"✅ Target hit on {index}: +{pnl:.2f}")
                log_exit(index, option_symbol, trade["entry_price"], ltp, "TARGET")
                total_pnl += pnl
                del active_trades[index]

            elif ltp <= trade["sl"]:
                pnl = ltp - trade["entry_price"]
                print(f"❌ SL hit on {index}: {pnl:.2f}")
                log_exit(index, option_symbol, trade["entry_price"], ltp, "SL")
                total_pnl += pnl
                del active_trades[index]

        time.sleep(60)

except Exception as e:
    print(f"❌ Bot Error: {e}")

finally:
    print("✅ Paper Bot Session Ended.")
