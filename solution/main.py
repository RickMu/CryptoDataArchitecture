from solution.DataCollector.Worker.IWorker import Worker
from solution.DataCollector.Schedular.Schedular import Schedular
from solution.Repository.OriginalDataSet.DataSet import DataSet
from solution.DataProcessor.DataProcessor import DataProcessor
from solution.DataCollector.Schedular.Tickers import Tickers
from solution.Repository.DataAccessor.DataSetAccessor import DataSetAccessor
from solution.DataObject.ComputedColumns import OriginalColumn

from solution.Repository.ComputedDataSet.ComputedDataSet import ComputedDataSet
from solution.Repository.DataAccessor.DataSetAccessor import DataSetAccessor
from solution.Repository.ComputedDataSet.RuleSet import RuleSet
from solution.Operators.Operator import OperatorType
from solution.DataObject.ComputedColumns import ComputedColumn

import time

if __name__ == "__main__":
    processor = DataProcessor()
    dataSet = DataSet(processor)
    accessor = DataSetAccessor(dataSet)


    configs = [
        (ComputedColumn.VOL_SUM, [(OriginalColumn.VOLUME, "")], OperatorType.SUM, 20),
        (ComputedColumn.MOMENTUM, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.DIFF, 20)
    ]
    computeddataset = ComputedDataSet()
    compdataaccessor = DataSetAccessor(computeddataset)
    ruleSet = RuleSet(computeddataset, accessor)
    ruleSet.createRules(configs)
    dataSet.addUpdateListener(ruleSet)


    configs = [
        (ComputedColumn.MOMENTUM_SUM, [(ComputedColumn.MOMENTUM, 20)], OperatorType.SUM, 20),
        (ComputedColumn.MOMENTUM_AVG, [(ComputedColumn.MOMENTUM, 20)], OperatorType.MOVAVG, 20)
    ]
    cd2 = ComputedDataSet()
    rs2 = RuleSet(cd2, compdataaccessor)
    rs2.createRules(configs)
    ruleSet.addUpdateListener(rs2)




    sch = Schedular()
    sch.setRequestConditions(Tickers.BITCOIN,(0,1))
    worker = Worker(consumer = dataSet, schedular=sch)
    worker.start()
    sch.start()






