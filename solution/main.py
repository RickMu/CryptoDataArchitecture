from solution.ConsumerProducerFrameWork.ConsumerProducer import Worker
from solution.DataCollector.Schedular.Schedular import Schedular
from solution.DataSet.OriginalDataSet.DataSet import DataSet
from solution.DataCollector.Schedular.Tickers import Tickers
from solution.DataObject.ComputedColumns import OriginalColumn
from solution.DataSet.ComputedDataSet.ComputedDataSet import ComputedDataSet
from solution.DataSet.DataAccessor.DataSetAccessor import DataSetAccessor
from solution.DataSet.ComputedDataSet.DataSetController import DataSetController
from solution.DataSet.ComputedDataSet.ComputedDataUpdateHandler import ComputedDataUpdateHandler
from solution.DataSet.ComputedDataSet.TechnicalIndicatorsFactory import TechnicalIndicatorsFactory

from solution.DataProcessor.DataProcessor import DataProcessor
from solution.DataSet.DataSetClient.Client import  Client
from solution.DataConsumer.RawDataConsumer import RawDataConsumer

if __name__ == "__main__":
    ds = ComputedDataSet()
    client = Client(ds)
    processor = DataProcessor()

    dataConsumer = RawDataConsumer(processor,client)

    schlr = Schedular()
    schlr.addConsumers(dataConsumer)
    schlr.setRequestConditions(Tickers.BITCOIN,(0,1))
    schlr.start()

    dataConsumer.start()






