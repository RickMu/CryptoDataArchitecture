
from DataObject.ComputedColumn import ComputedColumn, OriginalColumn
from Operators.Operator import OperatorType

MinInADay = 1440
class ComputedColumnLookUp:


    def __init__(self):
        self.__table={
            ComputedColumn.RSI: (OperatorType.RSI,([ComputedColumn.MOMENTUM,1])),
            ComputedColumn.MOMENTUM: (OperatorType.RSI,([OriginalColumn.PRICE_MEAN,0]))
        }
    
    Singleton = None

    def getRuleType(self, ruleType):
        if ruleType not in ComputedColumn or ruleType not in OriginalColumn:
             raise Exception("No Such Rule %s", str(ruleType))

        return self.__table[ruleType]

    @staticmethod
    def GetComputedColumn(ruleType, periods):
        if ComputedColumn.Singleton is None:
            ComputedColumn.Singleton = ComputedColumnLookUp()
        
        rule = ComputedColumnLookUp.Singleton.getRuleType(ruleType)
        
        
