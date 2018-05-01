import pandas as pd
from abc import abstractmethod
from solution.Operators.Operator import OperatorLookUp
from solution.DataObject.ComputedColumns import OriginalColumn
class RuleBase:

    def __init__(self,requiredColumns):
        self._requiredColumns = requiredColumns
        self._requiredColumnToIdentifiers()

    def _requiredColumnToIdentifiers(self):
        for pos in range(len(self._requiredColumns)):
            self._requiredColumns[pos] = self._toIdentifier(self._requiredColumns[pos])

    def _toIdentifier(self,tupleColumnRepresentation):
        if len(tupleColumnRepresentation) != 2:
            raise Exception("A Tuple Column Representation should be in the form of (Enum, period), Given: %s"
                            % (tupleColumnRepresentation))
        if tupleColumnRepresentation[1] == 0:
            return str(tupleColumnRepresentation[0])

        return str(tupleColumnRepresentation[0]) + str(tupleColumnRepresentation[1])

    @abstractmethod
    def compute(self,requiredData, updatedLength):
        return

class ColumnRule(RuleBase):
    
    def __init__(self,name, requiredColumns, operatorType, periods):
        RuleBase.__init__(self,requiredColumns)
        self._name = name
        self.__operatorType = operatorType 
        self.__operator = OperatorLookUp.GetOperator(self.__operatorType)
        self.__periods = periods

    def getIdentifier(self):
        return self._toIdentifier((self._name,self.__periods))

    def getPeriods(self):
        return self.__periods

    def checkOnRequiredColumns(self,data):
        for i in self._requiredColumns:
            if i not in data.keys():
                raise Exception("No Such column in Data: %s" % str(i))
        return True

    def compute(self,requiredData, updatedLength):
        self.checkOnRequiredColumns(requiredData)
        data = self.__operator(requiredData, self._requiredColumns, self.__periods)
        return data.iloc[len(data)-updatedLength:]

    def getRequiredColumns(self):
        return self._requiredColumns