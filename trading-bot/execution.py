from kiteconnect import KiteConnect
import os
import csv
import datetime
from config import API_KEY, API_SECRET, ACCESS_TOKEN, MIS_MARGIN

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

TRADE_LOG = "trade_log.csv"
_kite = None  # Global cache

def get_kite_client():
    global _kite
    if _kite is not None:
        return _kite

    kite.set_access_token(ACCESS_TOKEN)

    try:
        profile = kite.profile()
        print(f"✅ Logged in as: {profile['user_name']}")
    except Exception as e:
        print(f"❌ Access token check failed: {e}")
        exit(1)

    _kite = kite
    return kite

def log_trade(symbol, action, entry_price, exit_price, result, capital, reason, entry_reason):
    file_exists = os.path.isfile(TRADE_LOG)
    with open(TRADE_LOG, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "DateTime", "Stock", "Action", "Entry Price", "Exit Price",
                "Result", "PnL", "Capital After", "Exit Reason", "Entry Reason"
            ])
        pnl = round((exit_price - entry_price), 2) if result != "SKIPPED" else 0
        writer.writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            action,
            round(entry_price, 2),
            round(exit_price, 2),
            result,
            round(pnl, 2),
            round(capital, 2),
            reason,
            entry_reason
        ])

def get_market_data(stock):
    kite = get_kite_client()
    quote = kite.quote(f"NSE:{stock}")[f"NSE:{stock}"]
    return quote["last_price"], quote["ohlc"]["high"], quote["ohlc"]["low"]

def place_order(symbol, action, qty, entry_price):
    kite = get_kite_client()

    try:
        margin_info = kite.margins(segment="equity")
        available_cash = margin_info["available"]["cash"]
        margin_multiplier = MIS_MARGIN.get(symbol, 1)
        required_cash = (entry_price * qty) / margin_multiplier

        if required_cash > available_cash:
            print(f"⚠️ Skipped {symbol}: ₹{required_cash:.2f} needed, ₹{available_cash:.2f} available")
            return False
    except Exception as e:
        print(f"❌ Margin check failed: {e}")
        return False

    try:
        order = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=kite.TRANSACTION_TYPE_BUY if action == "BUY" else kite.TRANSACTION_TYPE_SELL,
            quantity=qty,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_MIS
        )
        print(f"✅ {action} order placed for {symbol}, Qty: {qty}")
        return True
    except Exception as e:
        print(f"❌ Order failed for {symbol}: {e}")
        return False
