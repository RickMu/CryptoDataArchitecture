import pandas as pd
from abc import abstractmethod
from solution.Operators.Operator import OperatorLookUp
from solution.DataObject.ComputedColumns import OriginalColumn
class RuleBase:
    
    @abstractmethod
    def compute(self,requiredData, periods, name,updatedLength):
        return

class ColumnRule(RuleBase):
    
    def __init__(self,requiredColumns, operatorType, periods):
        self.__requiredColumns = requiredColumns
        self.__operatorType = operatorType 
        self.__operator = OperatorLookUp.GetOperator(self.__operatorType)
        self.__periods = periods

    def getPeriods(self):
        return self.__periods

    def checkOnRequiredColumns(self,data):
        ret = True
        for i in self.__requiredColumns:
            if i not in data.keys():
                raise Exception("No Such column in Data: %s" % str(i))
        return True

    def compute(self,requiredData, updatedLength):
        self.checkOnRequiredColumns(requiredData)
        data = self.__operator(requiredData, self.__requiredColumns, self.__periods)
        return data.iloc[len(data)-updatedLength:]

    def getRequiredColumns(self):
        return self.__requiredColumns