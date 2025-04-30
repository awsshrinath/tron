from execution import get_market_data
from datetime import datetime
from config import RISK_PER_TRADE, MIS_MARGIN

def hybrid_strategy(stock, capital):
    price, high, low = get_market_data(stock)
    now = datetime.now().strftime('%H:%M')

    # Time filter
    if now < "09:25":
        return None

    range_size = high - low
    if range_size == 0:
        return None

    # Require price in upper 30% of range
    if price > (high + low) / 2 and (price - low) / range_size > 0.7:
        sl_per_share = max(price * 0.007, 6.0)  # 0.7% SL or minimum ₹6
        leverage = MIS_MARGIN.get(stock, 1)
        max_trade_cap = capital * 0.33 * leverage
        qty = int(RISK_PER_TRADE / sl_per_share)

        if qty * price > max_trade_cap:
            qty = int(max_trade_cap / price)
        if qty < 1:
            return None

        return {
            "action": "BUY",
            "entry": price,
            "target": price + sl_per_share * 2,
            "sl": price - sl_per_share,
            "qty": qty,
            "reason": "Hybrid Strategy"
        }

    return None
