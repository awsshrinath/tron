import sys
import os
from kiteconnect import KiteConnect

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import API_KEY, ACCESS_TOKEN

def get_kite_client():
    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(ACCESS_TOKEN)
    return kite

def get_market_data(symbol):
    kite = get_kite_client()
    try:
        if symbol in ["NIFTY", "BANKNIFTY"]:
            ltp = kite.ltp(f"NSE:{symbol}")[f"NSE:{symbol}"]["last_price"]
            return ltp, None, None, None  # Only LTP is available
        else:
            quote = kite.quote(f"NSE:{symbol}")[f"NSE:{symbol}"]
            return (
                quote["last_price"],
                quote["ohlc"]["high"],
                quote["ohlc"]["low"],
                quote["volume"]
            )
    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return None, None, None, None


def get_option_price(symbol):
    kite = get_kite_client()
    try:
        quote = kite.quote(f"NFO:{symbol}")[f"NFO:{symbol}"]
        return quote["last_price"]
    except Exception as e:
        print(f"❌ Error fetching option price for {symbol}: {e}")
        return None
