from queue import Queue
from solution.DataCollector.Schedular.Ec2ServerClient.EC2Client import EC2Client
from solution.DataCollector.Schedular.GdxClient.GdxClient import GdxClient
from threading import Thread
import time

class Schedular(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._dataQueue= Queue()
        self.EC2Client = EC2Client()
        self.GdxClient = GdxClient()
    def getData(self):
        if self._dataQueue.empty():
            return None
        return self._dataQueue.get()

    def setRequestConditions(self,tickers,timeSpan):
        self._tickers = tickers
        self._timeSpan = timeSpan
        self.EC2Client.setRequestConditions(self._tickers,self._timeSpan)
        self.GdxClient.setRequestConditions(self._tickers)
    def run(self):
        self.EC2Client.run()
        data = self.EC2Client.getReturnedData()
        self._dataQueue.put(data)
        self._getRealTimeData()
    def _getRealTimeData(self):
        while True:
            self.GdxClient.run()
            data = self.GdxClient.getReturnedData()
            self._dataQueue.put(data)
            time.sleep(5)



