import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils import get_nearest_itm_option, get_index_ltp
from volume_helper import is_volume_strong
from trend_helper import are_indices_aligned
from config import RISK_PER_TRADE

def scalper_strategy(index, capital):
    now = datetime.now().strftime('%H:%M')

    if now < "09:20" or now > "15:00":
        return None  # Trade only between 9:20 to 15:00

    # 🧠 Confirm trend alignment before checking options
    if not are_indices_aligned():
        print(f"❌ Skipping {index}: Nifty & BankNifty not aligned")
        return None

    trend = "UP"  # Can be made dynamic later
    spot_price = get_index_ltp(index)

    if not spot_price:
        print(f"❌ Skipping {index}: Could not fetch spot price")
        return None

    option_symbol, entry_price = get_nearest_itm_option(index, spot_price, trend=trend)

    if not option_symbol or not entry_price:
        print(f"❌ Skipping {index}: No matching ITM Option found")
        return None

    if not is_volume_strong(option_symbol):
        print(f"🔇 Skipping {option_symbol}: Weak volume")
        return None

    sl = 30
    target = 60
    qty = int(RISK_PER_TRADE / sl)

    print(f"✅ {option_symbol} selected for scalp: Entry ₹{entry_price}, Target ₹{entry_price + target}, SL ₹{entry_price - sl}")

    return {
        "option_symbol": option_symbol,
        "entry_price": entry_price,
        "target": entry_price + target,
        "sl": entry_price - sl,
        "qty": qty,
        "direction": "LONG",
        "reason": "Quick Scalping Strategy"
    }
