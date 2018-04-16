
from DataObject.ComputedColumns import ComputedColumn, OriginalColumn
from Operators.Operator import OperatorType, OperatorLookUp
from ColumnRules.ColumnRule import ColumnRule
from DataObject.ComputedDataObject import ComputedDataObject
MinInADay = 1440
class DataObjectFactory:


    def __init__(self, dataset, mediator):

        self._dataset = dataset
        self._mediator = mediator
        self.__table={
            ComputedColumn.RSI: (OperatorType.RSI,([ComputedColumn.MOMENTUM,1]), MinInADay),
            ComputedColumn.MOMENTUM: (OperatorType.DIFF,([OriginalColumn.PRICE_MEAN]),1),
            ComputedColumn.PRICE_STOK: (OperatorType.STOK,([OriginalColumn.PRICE_MEAN],[OriginalColumn.PRICE_MAX],[OriginalColumn.PRICE_MIN]),20)
        }
    def identifiersToNames(self,identifiers):
        names = []
        for i in identifiers:
            names.append(self.identifierToName(i))
        return names
    def identifierToName(self,identifier):
        if identifier[0] in OriginalColumn:
            return str(identifier[0])

        return str(identifier[0])+str(identifier[1])

    Singleton = None

    def getRuleType(self, ruleType):
        if ruleType not in ComputedColumn or ruleType not in OriginalColumn:
             raise Exception("No Such Rule %s", str(ruleType))

        if ruleType not in self.__table.keys():
            raise Exception("The Rule Type is not yet implemented %s" % str(ruleType))

        return self.__table[ruleType]


    
    def createComputedColumn(self,ruleType):
        ruleData = DataObjectFactory.Singleton.getRuleType(ruleType)
        operatorType = ruleData[0]
        rqCols =self.identifiersToNames(ruleData[1])
        period = ruleData[2]

        rule = ColumnRule(rqCols, operatorType, period)
        cdo = ComputedDataObject((ruleType,period),self._dataset, rule, self._mediator)

        return cdo

