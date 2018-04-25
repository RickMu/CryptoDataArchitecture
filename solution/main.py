from solution.DataCollector.Worker.IWorker import Worker
from solution.DataCollector.Schedular.Schedular import Schedular
from solution.DataSet.OriginalDataSet.DataSet import DataSet
from solution.DataSet.DataProcessor import DataProcessor
from solution.DataCollector.Schedular.Tickers import Tickers
from solution.DataObject.ComputedColumns import OriginalColumn
from solution.DataSet.ComputedDataSet.ComputedDataSet import ComputedDataSet
from solution.DataSet.DataAccessor.DataSetAccessor import DataSetAccessor
from solution.DataSet.ComputedDataSet.DataSetController import DataSetController
from solution.DataSet.ComputedDataSet.ComputedDataUpdateHandler import ComputedDataUpdateHandler
from solution.DataSet.ComputedDataSet.TechnicalIndicatorsFactory import TechnicalIndicatorsFactory
from solution.Operators.Operator import OperatorType
from solution.DataObject.ComputedColumns import ComputedColumn
from solution.DataSet.DataProcessor.DataProcessor import DataProcessor


def createRequiredComponents(subjectDataAccessor):
    dataset = ComputedDataSet()
    dataAccessor = DataSetAccessor(dataset)
    updateHandler = ComputedDataUpdateHandler(dataset,subjectDataAccessor)
    indicatorFactory = TechnicalIndicatorsFactory()

    dataSetController = DataSetController(dataset,indicatorFactory,updateHandler)
    return dataSetController,dataAccessor


if __name__ == "__main__":
    '''
    Note: All rows of data are minutely aggregated data 
    Cached data are data that is not aggregated minutely yet, 
    because the minute has not gone past, and so it's not sent to the dataset
    what is printed on the commandline are row counts
    
    Flow:
    Worker delivers data to DataSet 1, indicators that work with these data go into DataSet 2 and indicators that work
    with other indicators in DataSet 2 go into DataSet3 etc.
    '''
    processor = DataProcessor()
    dataSet = DataSet(processor)
    accessor = DataSetAccessor(dataSet)

    configs = [
        (ComputedColumn.VOL_SUM, [(OriginalColumn.VOLUME, "")], OperatorType.SUM, 20),
        (ComputedColumn.MOMENTUM, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.DIFF, 20),
        (ComputedColumn.PRICE_AVG, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.MOVAVG,20)
    ]
    c1,da1= createRequiredComponents(accessor)
    c1.initialize(configs)
    dataSet.addListeners(c1)

    configs = [
        (ComputedColumn.MOMENTUM_SUM, [(ComputedColumn.MOMENTUM, 20)], OperatorType.SUM, 20),
        (ComputedColumn.MOMENTUM_AVG, [(ComputedColumn.MOMENTUM, 20)], OperatorType.MOVAVG, 20)
    ]
    c2, da2 = createRequiredComponents(da1)
    c2.initialize(configs)
    c1.addListeners(c2)



    sch = Schedular()
    sch.setRequestConditions(Tickers.BITCOIN,(0,1))
    worker = Worker(consumer = dataSet, schedular=sch)
    worker.start()
    sch.start()






