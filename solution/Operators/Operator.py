
import pandas as pd
from enum import Enum
def rolling_rsi(values):
        up = values[values>0].mean()
        down = -1*values[values<0].mean()
        return 100 * up / (up + down)
    
def rolling_sum(values):
    return sum(values)

def rolling_avg(values):
    return rolling_sum(values)/len(values)

#Change positive then 1 else -1
def binarise_based_on_difference(values):
    change = values[0] - values[-1]
    if change == 0:
        return 0
    return change/abs(change)

def periodCountFromMax(values):
    maxPos = 0
    max = min(values)
    for pos in range(len(values)):
        if values[pos] >= max:
            maxPos = pos
            max = values[pos]

    return 100*(maxPos/len(values))

def periodCountFromMin(values):
    minPos = 0
    min = max(values)
    for pos in range(len(values)):
        if values[pos] <= min:
            minPos = pos
            min = values[pos]

    return 100*(minPos/len(values))

def aroonUp(data, inputCols, periods):
    inputname = inputCols[0]
    values = data[inputname].rolling(periods).apply(periodCountFromMax).fillna(0)
    return values

def aroonDown(data, inputCols, periods):
    inputname = inputCols[0]
    values = data[inputname].rolling(periods).apply(periodCountFromMin).fillna(0)
    return values

def rollingRSI(data,inputCols, periods):
    inputname = inputCols[0]
    values = data[inputname].rolling(periods).apply(rolling_rsi).fillna(0)
    return values


def rollingSum(data, inputCols, periods):
    inputname = inputCols[0]
    values = data[inputname].rolling(periods).apply(rolling_sum).fillna(0)
    return values

def movingAvg(data,inputCols ,periods):
    inputname = inputCols[0]
    values = data[inputname].rolling(periods).apply(rolling_avg).fillna(0)
    return values

def diff(data, inputCols ,periods):
    inputname = inputCols[0]
    values =  (data[inputname] - data[inputname].shift(periods)).fillna(0)
    return values

def diff_shift_otherway(data, inputCols, periods):
    inputname = inputCols[0]
    values = (data[inputname] - data[inputname].shift(-periods)).fillna(0)
    return values

def binariseColumnLeftDiff(data, inputCols, period):
    columnToBinarise = inputCols[0]

    binarised = data[columnToBinarise].rolling(period).apply(binarise_based_on_difference).fillna(0)

    return binarised

def SumAlignChange(data, inputCols, periods):
    binarisedColumn = inputCols[0]
    columnAlignOnChange = inputCols[1]
    alignedChange = data[columnAlignOnChange] * data[binarisedColumn]

    values = alignedChange.rolling(periods).apply(rolling_sum).fillna(0)
    return values



def stoK(data, inputCols, periods):
    curname = inputCols[0]
    maxname = inputCols[1]
    minname = inputCols[2]
    values = 100*((data[curname] - pd.rolling_min(data[minname],periods))
    /(pd.rolling_max(data[maxname],periods) - pd.rolling_min(data[minname],periods))).fillna(0)
    
    return values

def willR(data, inputCols,periods):
    curname = inputCols[0]
    maxname = inputCols[1]
    minname = inputCols[2]
    values = 100*((pd.rolling_max(data[minname],periods)- data[curname])
    /(pd.rolling_max(data[maxname],periods) - pd.rolling_min(data[minname],periods))).fillna(0)
    return values

def multiply(data,inputCols,periods):
    col1 = inputCols[0]
    col2 = inputCols[1]
    values = data[col1]*data[col2]
    return values

def subtract (data,inputCols,periods):
    subtractedFrom = inputCols[0]
    subtractor = inputCols[1]
    values = data[subtractedFrom] - data[subtractor]
    return values



class OperatorType(Enum):
    RSI = 1<<0
    SUM = 1<<1
    MOVAVG = 1<<2
    DIFF = 1<<3
    STOK = 1<<4
    WILLR = 1<<5
    MULTIPLY = 1<<6
    SUBTRACT = 1<<7
    AROON_UP = 1<<8
    AROON_DOWN = 1<<9
    SUM_ALIGN_CHANGE = 1<<10
    BINARISE_LEFT_DIFF = 1<<11

class OperatorLookUp:
    def __init__(self):

        self.__table={
            OperatorType.RSI: rollingRSI,
            OperatorType.SUM: rollingSum,
            OperatorType.MOVAVG: movingAvg,
            OperatorType.DIFF : diff,
            OperatorType.STOK: stoK,
            OperatorType.WILLR: willR,
            OperatorType.MULTIPLY: multiply,
            OperatorType.SUBTRACT: subtract,
            OperatorType.AROON_UP: aroonUp,
            OperatorType.AROON_DOWN:aroonDown,
            OperatorType.SUM_ALIGN_CHANGE:SumAlignChange,
            OperatorType.BINARISE_LEFT_DIFF: binariseColumnLeftDiff
        }
    
    Singleton = None

    def getOperator(self, operatorType):
        if operatorType not in OperatorType:
            raise Exception("No Such Operator %s", str(operatorType))
        return self.__table[operatorType]

    @staticmethod
    def GetOperator(operatorType):
        if OperatorLookUp.Singleton is None:
            OperatorLookUp.Singleton = OperatorLookUp()
        return OperatorLookUp.Singleton.getOperator(operatorType)
        


