from solution.DataCollector.Worker.IWorker import Worker
from solution.DataCollector.Schedular.Schedular import Schedular
from solution.Repository.OriginalDataSet.DataSet import DataSet
from solution.DataProcessor.DataProcessor import DataProcessor
from solution.DataCollector.Schedular.Tickers import Tickers

if __name__ == "__main__":
    processor = DataProcessor()
    dataSet = DataSet(processor)

    sch = Schedular()
    sch.setRequestConditions(Tickers.BITCOIN,(0,1))
    worker = Worker(consumer = dataSet, schedular=sch)
    worker.start()
    sch.start()

