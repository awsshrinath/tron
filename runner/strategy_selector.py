# runner/strategy_selector.py

class StrategySelector:
    def __init__(self, logger):
        self.logger = logger

    def select_strategy(self, market_data):
        sgx = market_data['sgx_nifty_change']
        dow = market_data['dow_futures_change']
        vix = market_data['india_vix_value']

        if sgx > 0.5 and dow > 0.5 and vix < 16:
            strategy = "Trend_Breakout"
        elif sgx < -0.5 and dow < -0.5 and vix < 16:
            strategy = "Trend_Breakdown"
        elif vix > 20:
            strategy = "Cautious_Reversal"
        else:
            strategy = "Range_Reversal"

        self.logger.log_event(f"Strategy Selected Based on Market Data: {strategy}")
        return strategy

# Test Mode
if __name__ == "__main__":
    print("StrategySelector class is ready!")
