import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from execution import get_market_data
from execution import get_kite_client
from utils import get_index_ltp

def are_indices_aligned():
    try:
        nifty_price = get_index_ltp("NIFTY")
        bank_price = get_index_ltp("BANKNIFTY")

        if nifty_price is None or bank_price is None:
            return False

        # Basic trend filter logic
        return nifty_price > 0 and bank_price > 0
    except Exception as e:
        print(f"❌ Trend check failed: {e}")
        return False
