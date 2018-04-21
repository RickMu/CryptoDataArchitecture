from solution.DataCollector.Worker.IWorker import Worker
from solution.DataCollector.Schedular.Schedular import Schedular
from solution.Mediator.Mediator import ComputedAndDataMediator
from solution.Repository.DataSet import DataSet
from solution.DataProcessor.DataProcessor import DataProcessor
from solution.DataCollector.Schedular.Tickers import Tickers

if __name__ == "__main__":
    processor = DataProcessor()
    mediator = ComputedAndDataMediator()
    dataSet = DataSet(processor,mediator)

    sch = Schedular()
    sch.setRequestConditions(Tickers.BITCOIN,(0,1))
    worker = Worker(consumer = dataSet, schedular=sch)
    worker.start()
    sch.start()
