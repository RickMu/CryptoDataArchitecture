from solution.DataCollector.Schedular.IClient.IDataTransformer import  ITransformer
import pandas as pd
from solution.DataCollector.Schedular.InputColumn import InputColumns
import datetime
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

        df = pd.DataFrame(data,dtype=float)
        self.__matchToInputEnum(df)
        df = self.__setTimeAsIndex(df)
        self.__calcBuySellVolData(df)
        df = self.__dropUnusedKeys(df)
        return df

    def __convertTimeFromUTC(self,df):
        #Pretty hacky method to get to UTC format
        # dates[pos][:16] is to cut off anything after %M in format
        dates = df[InputColumns.TIME].values
        FORMAT = '%Y-%m-%dT%H:%M'
        for pos in range(len(dates)):
            if dates[pos][-1] == 'Z':
                dt = datetime.datetime.strptime(dates[pos][:16],FORMAT)
                dt= dt+datetime.timedelta(hours=11)
                dates[pos] = datetime.datetime.strftime(dt,FORMAT)
        df[InputColumns.TIME] = dates

    def __matchToInputEnum(self,df):
        df[InputColumns.PRICE] = df[GdxColumns.PRICE]
        df[InputColumns.VOLUME] = df[GdxColumns.SIZE]
        df[InputColumns.TIME] = df[GdxColumns.TIME]
        self.__convertTimeFromUTC(df)

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







