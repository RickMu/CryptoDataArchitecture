
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
    data[col1] = data[col1]*data[col2]
    return data[col1]

class OperatorType(Enum):
    RSI = 1
    SUM = 2
    MOVAVG = 4
    DIFF = 8
    STOK = 16
    WILLR = 32
    MULTIPLY = 64

class OperatorLookUp:


    def __init__(self):

        self.__table={
            OperatorType.RSI: rollingRSI,
            OperatorType.SUM: rollingSum,
            OperatorType.MOVAVG: movingAvg,
            OperatorType.DIFF : diff,
            OperatorType.STOK: stoK,
            OperatorType.WILLR: willR,
            OperatorType.MULTIPLY: multiply
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
        


