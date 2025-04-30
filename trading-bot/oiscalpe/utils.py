from kiteconnect import KiteConnect
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from execution import get_kite_client
# Load Kite client using environment variables
kite = KiteConnect(api_key=os.getenv("ZERODHA_API_KEY"))
kite.set_access_token(os.getenv("ZERODHA_ACCESS_TOKEN"))

def get_ltp(symbol):
    try:
        quote = kite.ltp(symbol)
        return quote[symbol]["last_price"]
    except Exception as e:
        print(f"❌ Failed to fetch LTP for {symbol}: {e}")
        return None

def get_trend(symbol):
    try:
        data = kite.ohlc(symbol)
        ohlc = data[symbol]["ohlc"]
        return "UP" if ohlc["close"] > ohlc["open"] else "DOWN"
    except Exception as e:
        print(f"❌ Failed to fetch trend for {symbol}: {e}")
        return None

def get_index_ltp(symbol):
    """
    Fetch LTP for index using instrument_token.
    NIFTY: 256265
    BANKNIFTY: 260105
    """
    try:
        index_tokens = {
            "NIFTY": "NSE:NIFTY 50",
            "BANKNIFTY": "NSE:NIFTY BANK"
        }

        if symbol not in index_tokens:
            print(f"❌ Unknown index: {symbol}")
            return None

        quote = kite.ltp(index_tokens[symbol])
        return quote[index_tokens[symbol]]["last_price"]
    except Exception as e:
        print(f"❌ Error fetching index LTP for {symbol}: {e}")
        return None


def get_nearest_expiry(symbol):
    try:
        instruments = kite.instruments("NFO")
        today = datetime.now().date()

        expiries = sorted(set([
            inst["expiry"] for inst in instruments
            if inst["name"] == symbol and inst["segment"] == "NFO-OPT"
        ]))

        # Filter out past expiries
        future_expiries = [e for e in expiries if e >= today]
        if not future_expiries:
            raise Exception("No upcoming expiries found")

        return future_expiries[0]  # closest expiry
    except Exception as e:
        print(f"❌ Could not determine expiry for {symbol}: {e}")
        return None

def get_nearest_itm_option(base_symbol, spot_price, trend="UP", price_range=(100, 120)):
    try:
        expiry = get_nearest_expiry(base_symbol)
        if not expiry:
            print(f"❌ Could not determine expiry for {base_symbol}")
            return None, None

        option_type = "CE" if trend == "UP" else "PE"
        instruments = kite.instruments("NFO")
        candidates = [
            inst for inst in instruments
            if inst["name"] == base_symbol and
               inst["instrument_type"] == option_type and
               inst["expiry"] == expiry
        ]

        print(f"🔍 Checking {len(candidates)} options for {base_symbol} expiry {expiry}")

        for opt in candidates:
            try:
                ltp = kite.ltp(f"NFO:{opt['tradingsymbol']}")[f"NFO:{opt['tradingsymbol']}"]["last_price"]
                if price_range[0] <= ltp <= price_range[1]:
                    return f"NFO:{opt['tradingsymbol']}", ltp
            except:
                continue

        print(f"❌ No matching ITM Option found for {base_symbol}")
        return None, None
    except Exception as e:
        print(f"❌ Error in ITM option fetch: {e}")
        return None, None
