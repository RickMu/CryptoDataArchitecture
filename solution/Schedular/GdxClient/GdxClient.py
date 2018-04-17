from solution.Schedular.Tickers import Tickers
from solution.Schedular.GdxClient.GdxRequestBuilder import GdxApiBuilder
from threading import Thread
from solution.Schedular.IClient.IClient import IClient
import urllib.request
import json

class GdxClient(Thread, IClient):
    CB_BEFORE = 'cb-before'
    def __init__(self, listener):
        Thread.__init__(self)
        IClient.__init__(listener)
        self._cb_before = None
        self._tickerMap = {
            Tickers.BITCOIN: 'BTC-USD',
            Tickers.BCH: 'BCH-USD',
            Tickers.ETHER: 'ETH-USD',
            Tickers.LTC: 'LTC-USD'
        }
        self._requestBuilder = GdxApiBuilder()


    def run(self):
        self.fetchData()

    def _buildRequest(self,ticker):
        rq = None
        if self._cb_before is None:
            rq = self._requestBuilder.builFetchRequest(ticker)
        else:
            rq = self._requestBuilder.builFetchRequestGivenId(ticker, self._cb_before)
        return rq

    def _mapTicker(self,ticker):
        return self._tickerMap[ticker]

    def fetchData(self, ticker):
        ticker = self._mapTicker(ticker)
        request = self._buildRequest(ticker)

        with urllib.request.urlopen(request, timeout=20) as response:
            self._cb_before = response.headers[GdxClient.CB_BEFORE]
            data = json.load(response)
        self._listener.callback(data)
        return
