# runner/market_monitor.py

import requests
from bs4 import BeautifulSoup

class MarketMonitor:
    def __init__(self, logger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        })

    def fetch_sgx_nifty(self):
        try:
            url = 'https://www.investing.com/indices/singapore-msci-futures'
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            price_change_tag = soup.find('span', {'data-test': 'instrument-price-change-percent'})
            if price_change_tag:
                change_text = price_change_tag.text.strip().replace('%', '').replace('−', '-').replace('(', '').replace(')', '')
                percent_change = float(change_text)
                self.logger.log_event(f"Fetched SGX Nifty Change: {percent_change}%")
                return percent_change
            else:
                self.logger.log_event("SGX Nifty data not found.")
                return 0.0
        except Exception as e:
            self.logger.log_event(f"Error fetching SGX Nifty: {str(e)}")
            return 0.0

    def fetch_dow_futures(self):
        try:
            url = 'https://www.investing.com/indices/us-30-futures'
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            price_change_tag = soup.find('span', {'data-test': 'instrument-price-change-percent'})
            if price_change_tag:
                change_text = price_change_tag.text.strip().replace('%', '').replace('−', '-').replace('(', '').replace(')', '')
                percent_change = float(change_text)
                self.logger.log_event(f"Fetched Dow Futures Change: {percent_change}%")
                return percent_change
            else:
                self.logger.log_event("Dow Futures data not found.")
                return 0.0
        except Exception as e:
            self.logger.log_event(f"Error fetching Dow Futures: {str(e)}")
            return 0.0

    def fetch_india_vix(self):
        try:
            url = 'https://www.nseindia.com/market-data/indices-volatility'
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                vix_tag = soup.find('td', string='India VIX')
                if vix_tag:
                    value_tag = vix_tag.find_next('td')
                    vix_value = float(value_tag.text.strip())
                    self.logger.log_event(f"Fetched India VIX Value: {vix_value}")
                    return vix_value
                else:
                    self.logger.log_event("India VIX not found on page. Using fallback value 15.")
                    return 15.0
            else:
                self.logger.log_event("Failed to fetch VIX page, fallback to 15.")
                return 15.0
        except Exception as e:
            self.logger.log_event(f"Error fetching India VIX: {str(e)}")
            return 15.0

    def fetch_premarket_data(self):
        self.logger.log_event("Fetching Real Pre-Market Data...")
        sgx_nifty_change = self.fetch_sgx_nifty()
        dow_futures_change = self.fetch_dow_futures()
        india_vix_value = self.fetch_india_vix()

        premarket_data = {
            "sgx_nifty_change": sgx_nifty_change,
            "dow_futures_change": dow_futures_change,
            "india_vix_value": india_vix_value,
            "nifty_preopen_change": sgx_nifty_change  # Using SGX as proxy if pre-open not available
        }
        return premarket_data
