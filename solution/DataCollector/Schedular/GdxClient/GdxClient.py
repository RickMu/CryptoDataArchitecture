from solution.DataCollector.Schedular.Tickers import Tickers
from solution.DataCollector.Schedular.GdxClient.GdxRequestBuilder import GdxApiBuilder
from solution.DataCollector.Schedular.IClient.IClient import IClient
from solution.DataCollector.Schedular.GdxClient.GdxDataTransformer import GdxDataTransformer
import urllib.request
import json

class GdxTickersMap:
    GdxTickers = {
        Tickers.BITCOIN: 'BTC-USD',
        Tickers.BCH: 'BCH-USD',
        Tickers.ETHER: 'ETH-USD',
        Tickers.LTC: 'LTC-USD'
    }


class GdxClient(IClient):
    PAGINATION_KEY = 'cb-before'

    def __init__(self):
        self._cb_before = None
        self._requestBuilder = GdxApiBuilder()
        self._dataTransformer = GdxDataTransformer()
        self._ticker = None

    def setRequestConditions(self, ticker,timeSpan = None):
        self._ticker = ticker

    def run(self):
        self.fetchData(self._ticker)

    def __buildRequest(self,ticker):
        #if there is no trade identifier then just send a casual request
        rq = None
        if self._cb_before is None:
            rq = self._requestBuilder.builFetchRequest(ticker,timeSpan = None)
        else:
            rq = self._requestBuilder.builFetchRequestGivenId(ticker, self._cb_before)
        print(rq)
        return rq

    def __mapTicker(self,ticker):
        return GdxTickersMap.GdxTickers[ticker]
    def __parseResponse(self,request):
        with urllib.request.urlopen(request, timeout=20) as response:
            #loads the next identifier that is needed to make the request
            data = json.load(response)
            if data != []:
                self._cb_before = response.headers[GdxClient.PAGINATION_KEY]
            return data

    def fetchData(self, ticker, timeSpan= None):
        ticker = self.__mapTicker(ticker)
        request = self.__buildRequest(ticker)
        data = self.__parseResponse(request)
        if data == []:
            self._returnedData= None
            return
        dataframe = self._dataTransformer.mapInputToRequiredOutput(data)
        self._returnedData = dataframe

if __name__ == '__main__':

    gdxClient = GdxClient()
    gdxClient.setRequestConditions(Tickers.BITCOIN)
    gdxClient.run()
    print(gdxClient.getReturnedData())
    gdxClient.run()
    print(gdxClient.getReturnedData())
