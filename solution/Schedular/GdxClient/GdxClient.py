from solution.Schedular.Tickers import Tickers
from solution.Schedular.GdxClient.GdxRequestBuilder import GdxApiBuilder
from threading import Thread
from solution.Schedular.IClient.IClient import IClient
from solution.Schedular.GdxClient.GdxDataTransformer import GdxDataTransformer
import urllib.request
import json

class GdxTickersMap:
    GdxTickers = {
        Tickers.BITCOIN: 'BTC-USD',
        Tickers.BCH: 'BCH-USD',
        Tickers.ETHER: 'ETH-USD',
        Tickers.LTC: 'LTC-USD'
    }


class GdxClient(Thread, IClient):
    PAGINATION_KEY = 'cb-before'

    def __init__(self, listener):
        Thread.__init__(self)
        IClient.__init__(listener)
        self._cb_before = None
        self._requestBuilder = GdxApiBuilder()
        self._processor = GdxProcessor()

    def run(self):
        self.fetchData()

    def __buildRequest(self,ticker):
        #if there is no trade identifier then just send a casual request
        rq = None
        if self._cb_before is None:
            rq = self._requestBuilder.builFetchRequest(ticker)
        else:
            rq = self._requestBuilder.builFetchRequestGivenId(ticker, self._cb_before)
        return rq

    def __mapTicker(self,ticker):
        return GdxTickersMap.GdxTickers[ticker]

    def fetchData(self, ticker):
        ticker = self.__mapTicker(ticker)
        request = self.__buildRequest(ticker)

        with urllib.request.urlopen(request, timeout=20) as response:
            #loads the next identifier that is needed to make the request
            self._cb_before = response.headers[GdxClient.PAGINATION_KEY]
            data = json.load(response)
        self._listener.callback(data)
        return

if __name__ == '__main__':

    import pandas as pd
    builder = GdxApiBuilder()
    rq1 = builder.builFetchRequest('BTC-USD')
    rq2 = builder.builFetchRequestGivenId('BitCOIN', 12321)
    print(rq1)
    print(rq2)

    with urllib.request.urlopen(rq1, timeout=20) as response:
        print(response.headers['cb-before'])

        data = json.load(response)
        df = pd.DataFrame(data)

        transformer = GdxDataTransformer()
        df = transformer.mapInputToRequiredOutput(data)

        print(df)
