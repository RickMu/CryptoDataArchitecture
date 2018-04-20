from abc import abstractmethod
from solution.DataCollector.Schedular.Tickers import Tickers
import time
class IWorker:

    def __init__(self,dataset):
        #datasource to feed collected data into
        self.dataset = dataset

    @abstractmethod
    def collectData(self):
        return

class Worker(IWorker):

    def __init__(self,dataset,schedular):
        IWorker.__init__(self,dataset)
        self.schedular = schedular

    def collectData(self):
        while True:
            data = self.schedular.getData()
            if data is not None:
                print(data)
            time.sleep(5)

if __name__ == '__main__':
    from solution.DataCollector.Schedular.Schedular import Schedular
    sch = Schedular()
    sch.setRequestConditions(Tickers.BITCOIN,(0,1))
    sch.start()

    worker = Worker(None,sch)
    worker.collectData()
