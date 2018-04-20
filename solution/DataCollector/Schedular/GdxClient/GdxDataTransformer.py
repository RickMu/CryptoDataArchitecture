from solution.DataCollector.Schedular.IClient.IDataTransformer import  ITransformer
import pandas as pd
from solution.DataCollector.Schedular.InputColumn import InputColumns
from collections import defaultdict

class GdxColumns:
    PRICE = 'price'
    SIDE = 'side'
    SIZE = 'size'
    TIME = 'time'
    TRADE_ID = 'trade_id' # trade_id is ignored

class SideColumnValues:
    BUY = 'buy'
    SELL = 'sell'

class GdxDataTransformer(ITransformer):

    def mapInputToRequiredOutput(self,data):
        #CoinBase Api returns data in json format
        if not data:
            return None
        df = pd.DataFrame(data)
        self.__matchToInputEnum(df)
        df = self.__setTimeAsIndex(df)
        self.__calcBuySellVolData(df)
        df = self.__dropUnusedKeys(df)
        return df

    def __matchToInputEnum(self,df):
        df[InputColumns.PRICE] = df[GdxColumns.PRICE]
        df[InputColumns.VOLUME] = df[GdxColumns.SIZE]
        df[InputColumns.TIME] = df[GdxColumns.TIME]

    def __setTimeAsIndex(self,df):
        df = df.set_index(InputColumns.TIME)
        return df

    def __dropUnusedKeys(self,df):
        unusedKeys = []
        for gdxKeys in df.keys():
            if gdxKeys not in InputColumns:
                unusedKeys.append(gdxKeys)
        df = df.drop(columns=unusedKeys)
        return df

    def __calcBuySellVolData(self, df):

        df[InputColumns.BUY_VOL] = (df[GdxColumns.SIDE] == SideColumnValues.BUY ).astype(int) *df[GdxColumns.SIZE]
        df[InputColumns.SELL_VOL] = (df[GdxColumns.SIDE] == SideColumnValues.SELL).astype(int) * df[GdxColumns.SIZE]







