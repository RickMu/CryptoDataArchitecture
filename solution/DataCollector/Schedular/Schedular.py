from solution.DataCollector.Schedular.Ec2ServerClient.EC2Client import EC2Client
from solution.DataCollector.Schedular.GdxClient.GdxClient import GdxClient
import time
from solution.ConsumerProducerFrameWork.ConsumerProducer import Collector

class Schedular(Collector):

    def __init__(self,queue):
        Collector.__init__(self,queue)
        self.EC2Client = EC2Client()
        self.GdxClient = GdxClient()

    def setRequestConditions(self,tickers,timeSpan):
        self._tickers = tickers
        self._timeSpan = timeSpan
        self.EC2Client.setRequestConditions(self._tickers,self._timeSpan)
        self.GdxClient.setRequestConditions(self._tickers)

    def run(self):
        self.EC2Client.run()
        data = self.EC2Client.getReturnedData()
        self._addToQueue(data)
        self._getRealTimeData()

    def _getRealTimeData(self):
        while True:
            self.GdxClient.run()
            data = self.GdxClient.getReturnedData()
            if data is not None:
                self._addToQueue(data)
            time.sleep(5)



