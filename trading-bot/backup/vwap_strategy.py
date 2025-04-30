from execution import get_market_data
from config import RISK_PER_TRADE, MIS_MARGIN
from datetime import datetime

def vwap_strategy(stock, capital):
    price, high, low = get_market_data(stock)
    now = datetime.now().strftime('%H:%M')
    if now < "09:25":
        return None

    vwap = (high + low + price) / 3  # Simulated VWAP

    if price > vwap and (price - low) / (high - low) > 0.7:
        sl_per_share = max(price * 0.007, 6.0)
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
            "reason": "VWAP Reversal (VWAP Strategy)"
        }

    return None
