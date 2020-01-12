import json
import requests

from apis.StockDataProvider import StockDataSource


class WtdsDataSource(StockDataSource):

    def __init__(self):

        self.apikey = "xfcqGEwXwqrz4sVnriDVatbsMf5Lhs37LDkwO38Jq3MK6XyvOieQDTrHhM7M"
        self.limit = 250
        super(WtdsDataSource, self).__init__(self.apikey, self.limit)

    def get_live(self, symbol):
        data = {
            "symbol" : symbol,
            "api_token" : self.apikey,
        }

        #data = json.dumps(data)

        #URL = "http://intraday.worldtradingdata.com/api/v1/stock/?symbol=SPCE&interval=1&range=7&api_token=xfcqGEwXwqrz4sVnriDVatbsMf5Lhs37LDkwO38Jq3MK6XyvOieQDTrHhM7M"
        URL = "http://intraday.worldtradingdata.com/api/v1/stock"
        r = requests.get(url=URL, params=data)
        return r.json()

    def get_intraday(self, symbol, interval, range):
        data = {
            "symbol"    : symbol,
            "api_token" : self.apikey,
            "interval"  : interval,
            "range"     : range,
        }

        #URL = "http://intraday.worldtradingdata.com/api/v1/intraday/?symbol=SPCE&interval=5&range=30&api_token=xfcqGEwXwqrz4sVnriDVatbsMf5Lhs37LDkwO38Jq3MK6XyvOieQDTrHhM7M&output=csv"
        URL = "http://intraday.worldtradingdata.com/api/v1/intraday"
        r = requests.get(url=URL, params=data)

        return r

    def get_history(self, symbol):
        data = {
            "symbol"    : symbol,
            "api_token" : self.apikey,
        }

        URL = "https://api.worldtradingdata.com/api/v1/history"
        r = requests.get(url=URL, params=data)

        return r