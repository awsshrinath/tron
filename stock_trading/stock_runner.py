import os
import sys
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from runner.utils.instrument_utils import get_kite_client, get_instrument_tokens
from runner.trade_manager import execute_trade
from runner.config import PAPER_TRADE
from runner.trade_manager import simulate_exit

# --- Strategy ---
from stock_trading.strategies.vwap_strategy import vwap_strategy


def get_realtime_stock_data(kite, symbols):
    token_map = get_instrument_tokens(symbols)
    data_list = []

    for symbol in symbols:
        token = token_map.get(symbol)
        if not token:
            continue
        data_list.append({"symbol": symbol, "token": token})

    return data_list


def run_stock_trading_bot():
    print("[INFO] Starting Stock Trading Bot...")
    kite = get_kite_client()
    symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "SBIN"]
    instruments = get_realtime_stock_data(kite, symbols)

    for data in instruments:
        from_date = datetime.now() - timedelta(minutes=60)
        to_date = datetime.now()

        try:
            candles = kite.historical_data(data["token"], from_date, to_date, interval="5minute")
        except Exception as e:
            print(f"[ERROR] Failed to fetch candles for {data['symbol']}: {e}")
            continue

        trade = vwap_strategy(data["symbol"], candles, capital=10000)
        if trade:
            trade["strategy"] = "vwap"
            execute_trade(trade, paper_mode=PAPER_TRADE)
        else:
            print(f"[WAIT] No valid VWAP trade signal found for {data['symbol']}.")

        if PAPER_TRADE:
            exit_candles = kite.historical_data(trade["symbol"], trade["entry_time"], "15:20", interval="5minute")
            simulate_exit(trade, exit_candles)


if __name__ == "__main__":
    run_stock_trading_bot()
