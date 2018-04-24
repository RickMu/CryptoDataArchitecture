from solution.Repository.IDataSet.IDataUpdateListener import IDataUpdateListener
from solution.DataObject.ComputedColumns import OriginalColumn,ComputedColumn
from solution.ColumnRules.ColumnRule import ColumnRule
from solution.Operators.Operator import OperatorType
from abc import abstractmethod
from collections import defaultdict
from threading import Thread
import pandas as pd
class IRuleSet(IDataUpdateListener):
    def __init__(self,dataset,dataReader):
        self._rules = []
        self._dataset = dataset
        self._dataReader = dataReader
        self._listener = None

    def _notifyListener(self,updatedLength):
        if self._listener is not None:
            self._listener.notify(updatedLength)

    def addUpdateListener(self,listener):
        self._listener = listener

    def notify(self, updatedLength):
        threads = []
        for rule in self._rules:
            t = Thread(target=self._updateColumn, args=(rule, updatedLength))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        self._notifyListener(updatedLength)
        return

    def _updateColumn(self,rule,updatedLength):
        data = self._getRequiredData(rule, updatedLength)
        data = rule.compute(data, updatedLength)
        self._dataset.updateColumn(rule.getIdentifier(), data)

    @abstractmethod
    def createRules(self,configs):
        return

    @abstractmethod
    def _getRequiredData(self,rule,updateLength):
        return

from threading import Thread

class RuleSet(IRuleSet):

    def __init__(self,dataset,dataReader):
        IRuleSet.__init__(self,dataset,dataReader)

        # Needs Checking
    def createRules(self,configs):
        for i in configs:
            self._createRule(i)

    def _createRule(self,config):
        #self.__configsCheck(config)
        rule = ColumnRule(config[0],config[1],config[2],config[3])
        self._rules.append(rule)
        self._dataset.addColumn(rule.getIdentifier())

    def _getRequiredData(self, rule, updatedLength):
        rqCols = rule.getRequiredColumns()
        data = defaultdict(pd.Series)
        for col in rqCols:
            data[col] = self._dataReader.read(col, updatedLength + rule.getPeriods())
        return data

    def __checkColumns(self, columns):
        for i in columns:
            if i[0] not in OriginalColumn:
                raise Exception("This RuleSet is only mean for Original Column aggregates")

    def __checkOperator(self, name):
        if name not in OperatorType:
            raise Exception("Operator is not OperatorType %s" % (name))

    def __configsCheck(self, config):
        if len(config) != 4:
            raise Exception("Config has to contain a list of needed columns, operator, and period")
        self.__checkColumns(config[1])
        self.__checkOperator(config[2])

if __name__ == "__main__":
    from solution.Repository.ComputedDataSet.ComputedDataSet import ComputedDataSet
    from solution.Repository.DataAccessor.DataSetAccessor import DataSetAccessor
    dataset = ComputedDataSet()
    dataccessor = DataSetAccessor(dataset)
    ruleSet = RuleSet(dataset,dataccessor)
    configs = [
        (ComputedColumn.VOL_SUM,[(OriginalColumn.VOLUME,"")],OperatorType.SUM,20),
        (ComputedColumn.MOMENTUM, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.DIFF, 20)
    ]
    ruleSet.createRules(configs)
    print(dataset.getColumnNames())


