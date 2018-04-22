from abc import abstractmethod
from solution.DataCollector.Schedular.Tickers import Tickers
from threading import Thread
import time
class IWorker:

    def __init__(self,consumer):
        #datasource to feed collected data into
        self._consumer = consumer

    @abstractmethod
    def collectData(self):
        return

class Worker(IWorker, Thread):

    def __init__(self,consumer,schedular):
        Thread.__init__(self)
        IWorker.__init__(self,consumer)
        self.schedular = schedular

    def run(self):
        self.collectData()

    def collectData(self):
        while True:
            if self._consumer.isReadyToConsume():
                data = self.schedular.getData()
                if data is not None:
                    self._consumer.consume(data)
            time.sleep(5)

if __name__ == '__main__':
    from solution.DataCollector.Schedular.Schedular import Schedular
    sch = Schedular()
    sch.setRequestConditions(Tickers.BITCOIN,(0,1))
    sch.start()
    worker = Worker(None,sch)
    worker.collectData()
