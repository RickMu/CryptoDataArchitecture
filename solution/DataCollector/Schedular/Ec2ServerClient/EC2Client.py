from solution.DataCollector.Schedular.Tickers import Tickers
from threading import Thread
from solution.DataCollector.Schedular.IClient.IClient import IClient
from solution.DataCollector.Schedular.Ec2ServerClient.Ec2RequestBuilder import Ec2RequestBuilder
from solution.DataCollector.Schedular.Ec2ServerClient.Ec2DataTransformer import Ec2DataTransformer
import urllib.request
import solution.server.cointrade_pb2 as cointrade_pd
import pandas as pd


class EC2TickersMap:
    EC2Tickers = {
        Tickers.BITCOIN: 'BTC-USD',
        Tickers.BCH: 'BCH-USD',
        Tickers.ETHER: 'ETH-USD',
        Tickers.LTC: 'LTC-USD'
    }


class EC2Client( IClient):

    def __init__(self):
        self._requestBuilder = Ec2RequestBuilder()
        self._dataTransformer = Ec2DataTransformer()
        self._ticker = None
        self._timeSpan = None

    # Best not exceed 10 days of timespan, because the data is way too large and takes ages
    def setTimeSpan(self, days, hours):
        self.days = days
        self.hours = hours

    def setRequestConditions(self, ticker, timeSpan=None):
        self._ticker = ticker
        self._timeSpan = timeSpan

    def run(self):
        self.fetchData(self._ticker, self._timeSpan)

    def __mapTicker(self, ticker):
        return EC2TickersMap.EC2Tickers[ticker]

    def __requestEndPoint(self, request):
        with urllib.request.urlopen(request) as response:
            data = response.read()
            return data


    def fetchData(self, ticker, timeSpan=None):
        if timeSpan is None:
            raise Exception("For EC2 Queries time span is needed")

        ticker = self.__mapTicker(ticker)
        requests = self._requestBuilder.buildFetchRequest(ticker, timeSpan)
        print(requests)

        dfs = pd.DataFrame()
        for request in requests:
            data = self.__requestEndPoint(request)
            if data == []:
                self._returnedData = None
                return

            trades = cointrade_pd.Trades()
            trades.ParseFromString(data)
            dataframe = self._dataTransformer.mapProtoBufferInputToOutput(trades)
            dfs = dfs.append(dataframe)
        self._returnedData = dfs


if __name__ == '__main__':
    from solution.DataCollector.Schedular.InputColumn import InputColumns
    client = EC2Client()
    client.setRequestConditions(Tickers.BITCOIN, (2, 1))
    client.run()
    df = client.getReturnedData()
    df.sort_index(inplace= True)
    print(df)
    df.groupby(df.index)\
        .agg({InputColumns.PRICE: ['min', 'max', 'mean'], InputColumns.VOLUME: 'sum'})
