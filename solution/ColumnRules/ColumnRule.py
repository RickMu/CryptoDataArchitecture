import pandas as pd
from abc import abstractmethod
from Operators.Operator import OperatorLookUp
class RuleBase:
    
    @abstractmethod
    def compute(self,requiredData, periods, name,updatedLength):
        return
    
class ColumnRule(RuleBase):
    
    def __init__(self,requiredColumns, ruleType):
        self.__requiredColumns = requiredColumns
        self.__ruleType = ruleType 
    
    def checkOnRequiredColumns(self,data):
        ret = True
        for i in self.__requiredColumns:
            if i not in data.keys():
                return False
        return True

    def compute(self,requiredData, periods, name,updatedLength):
        self.checkOnRequiredColumns(requiredData)
        operator = OperatorLookUp.GetOperator(self.__ruleType)
        data = operator(requiredData, 'PriceMean', periods)
        return data[data.size-updatedLength:]

    def getRequiredColumns(self):
        return self.__requiredColumns