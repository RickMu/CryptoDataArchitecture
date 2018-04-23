from solution.Repository.IDataSet.IDataUpdateListener import IDataUpdateListener
from solution.DataObject.ComputedColumns import OriginalColumn,ComputedColumn
from solution.ColumnRules.ColumnRule import ColumnRule
from solution.Operators.Operator import OperatorType
from abc import abstractmethod
from collections import defaultdict
class IRuleSet(IDataUpdateListener):


    @abstractmethod
    def createRules(self,configs):
        return


class RuleSet(IRuleSet):
    Single_Event = "Original"

    def __init__(self):
        self._rules = None
        self._eventMap = defaultdict(list)

    def createRulesFromMap(self):
        self.createRules(None)

    def __checkColumns(self, columns):
        for i in columns:
            if i not in OriginalColumn:
                raise Exception("This RuleSet is only mean for Original Column aggregates")

    def __checkOperator(self, name):
        if name not in OperatorType:
            raise Exception("Operator is not OperatorType %s" %(name))

    def __configsCheck(self,config):
        if len(config) != 3:
            raise Exception("Config has to contain a list of needed columns, operator, and period")
        self.__checkColumns(config[0])
        self.__checkOperator(config[1])

    def __registerRule(self,rule,config):
        self._eventMap[RuleSet.Single_Event].append(rule)

    def createRules(self,config):
        self.__configsCheck(config)
        rule = ColumnRule(config[0],config[1],config[2])
        self.__registerRule(rule,config)

    def notify(self,key,data):
        return




