from solution.DataCollector.Schedular.IClient.IDataTransformer import ITransformer
import pandas as pd
from solution.DataCollector.Schedular.InputColumn import InputColumns

class EC2Columns:
    PRICE = 'price'
    TREND = 'trend'
    TIME = 'created_at'
    MONGO_ID = '_id'
    GDX_ID = 'id'
    SIDE = 'side' #this is buy or sell for EC2
    VOLUME = 'volume'

class SideColumnValues:
    BUY = 'buy'
    SELL = 'sell'

class Ec2DataTransformer(ITransformer):
    def mapProtoBufferInputToOutput(self,trades):
        jsons = []
        for trade in trades.trades:
            json= {}
            json[EC2Columns.PRICE] = trade.price
            json[EC2Columns.VOLUME] = trade.volume
            json[EC2Columns.TIME] = trade.created_at
            json[EC2Columns.TREND] = trade.trend
            json[EC2Columns.GDX_ID] = trade.id
            json[EC2Columns.SIDE] = trade.side
            jsons.append(json)

        return self.mapInputToRequiredOutput(jsons)

    def mapInputToRequiredOutput(self,data):
        #EC2 Api returns data in json format
        df = pd.DataFrame(data,dtype=float)
        self.__matchToInputEnum(df)
        df = self.__setTimeAsIndex(df)
        self.__calcBuySellVolData(df)
        df = self.__dropUnusedKeys(df)
        return df

    def __matchToInputEnum(self,df):
        df[InputColumns.PRICE] = df[EC2Columns.PRICE]
        df[InputColumns.VOLUME] = df[EC2Columns.VOLUME]
        df[InputColumns.TIME] = df[EC2Columns.TIME]

    def __setTimeAsIndex(self,df):
        df = df.set_index(InputColumns.TIME)
        return df

    def __dropUnusedKeys(self,df):
        unusedKeys = []
        for ec2Keys in df.keys():
            if ec2Keys not in InputColumns:
                unusedKeys.append(ec2Keys)
        df = df.drop(columns=unusedKeys)
        return df

    def __calcBuySellVolData(self, df):
        df[InputColumns.BUY_VOL] = (df[EC2Columns.SIDE] == SideColumnValues.BUY ).astype(int) *df[EC2Columns.VOLUME]
        df[InputColumns.SELL_VOL] = (df[EC2Columns.SIDE] == SideColumnValues.SELL).astype(int) * df[EC2Columns.VOLUME]

