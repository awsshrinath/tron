from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from execution import get_market_data  # or whatever module you're importing

def get_near_month_contract(stock_symbol):
    """
    Generate the correct near-month futures symbol like NIFTY24APRFUT
    """
    now = datetime.now()
    year_suffix = str(now.year)[2:]  # '24'
    month_abbr = now.strftime("%b").upper()  # 'APR'

    return f"{stock_symbol}{year_suffix}{month_abbr}FUT"
