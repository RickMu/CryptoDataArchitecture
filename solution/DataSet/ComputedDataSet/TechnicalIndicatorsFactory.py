from abc import abstractmethod
from solution.ColumnRules.ColumnRule import ColumnRule
from solution.DataObject.ComputedColumns import OriginalColumn
from solution.Operators.Operator import OperatorType
from solution.DataSet.IDataSet.IFactory import IFactory


class TechnicalIndicatorsFactory(IFactory):

    def create(self,configs):
        #self.__configsCheck(config)
        indicators = []
        for config in configs:
            indicator = self._createIndicator(config)
            indicators.append(indicator)
        return indicators

    def _createIndicator(self,config):
        indicator = ColumnRule(config[0], config[1], config[2], config[3])
        return indicator

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
