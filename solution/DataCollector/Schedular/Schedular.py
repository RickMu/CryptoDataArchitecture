import time
from threading import Thread

from solution.DataCollector.BaseDataProvider import BaseDataProvider
from solution.DataCollector.Schedular.Ec2ServerClient.EC2Client import EC2Client
from solution.DataCollector.Schedular.GdxClient.GdxClient import GdxClient


class Schedular(BaseDataProvider):

    def __init__(self):
        Thread.__init__(self)
        self.EC2Client = EC2Client()
        self.GdxClient = GdxClient()
        self.consumers = []

    def addConsumers(self,consumer):
        self.consumers.append(consumer)

    def onDataObtained(self, data):
        for consumer in self.consumers:
            consumer.consume(data)

    def setRequestConditions(self,tickers,timeSpan):
        self._tickers = tickers
        self._timeSpan = timeSpan
        self.EC2Client.setRequestConditions(self._tickers,self._timeSpan)
        self.GdxClient.setRequestConditions(self._tickers)

    def run(self):
        self.EC2Client.run()
        data = self.EC2Client.getReturnedData()
        self.onDataObtained(data)
        self._getRealTimeData()

    def _getRealTimeData(self):
        while True:
            try:
                self.GdxClient.run()

                data = self.GdxClient.getReturnedData()
                if data is not None:
                    self.onDataObtained(data)
            except:
                print("exception")

            time.sleep(5)



