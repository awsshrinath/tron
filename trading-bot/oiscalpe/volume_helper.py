import sys
import os
from kiteconnect import KiteConnect

kite = KiteConnect(api_key=os.getenv("ZERODHA_API_KEY"))
kite.set_access_token(os.getenv("ZERODHA_ACCESS_TOKEN"))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from execution import get_market_data  # or actual volume-fetching if integrated

# Set realistic volume thresholds for option contracts
MIN_OPTION_VOLUME = 50000  # You can tune this based on performance

def is_volume_strong(symbol):
    try:
        quote = kite.quote(symbol)
        volume = quote[symbol]["volume"]
        if volume is None:
            raise ValueError("Volume is None")
        return volume >= 100000
    except Exception as e:
        print(f"❌ Volume check failed for {symbol}: {e}")
        return False
