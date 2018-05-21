from solution.DataCollector.Schedular.Schedular import Schedular
from solution.DataCollector.Schedular.Tickers import Tickers
from solution.DataSet.ComputedDataSet.ComputedDataSet import ComputedDataSet

from solution.DataProcessor.DataProcessor import DataProcessor
from solution.DataSetClient import  DataEntry
from solution.DataConsumer.DataSetConsumer.RealTimeDataConsumer import RawDataConsumer

if __name__ == "__main__":
    ds = ComputedDataSet()
    client = DataEntry(ds)
    processor = DataProcessor()

    dataConsumer = RawDataConsumer(processor,client)

    schlr = Schedular()
    schlr.addConsumers(dataConsumer)
    schlr.setRequestConditions(Tickers.BITCOIN,(0,1))
    schlr.start()

    dataConsumer.start()






