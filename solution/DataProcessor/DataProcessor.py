import pandas as pd
from solution.DataObject.ComputedColumns import OriginalColumn
from solution.DataCollector.Schedular.InputColumn import InputColumns
from solution.DataProcessor.contracts.IProcessor import IProcessor

class DataProcessor(IProcessor):
    
    def __init__(self):
        self.__cachedData = pd.DataFrame()
        
    #Gets the last minute data, 
    #and returns all data before the last minute for correct aggregation
    def __preProcessData(self, datasource):
        datasource.sort_index(inplace=True)
        index = datasource.index.values
        earliestTime = index[0]
        latestedTime= index[-1]

        if earliestTime> latestedTime:
            raise Exception("earliest time %s , is greater than latest time %s" % (earliestTime,latestedTime))
        print(latestedTime)
        datasource = self.__cachedData.append(datasource)
        datasource.sort_index(inplace=True)
        data = datasource[datasource.index < latestedTime]
        self.__cachedData = datasource[datasource.index >= latestedTime]

        print("*********************************Cached Data********************************")
        print(self.__cachedData.shape[0])
        return data
    
    def getCachedData(self):
        return self.__cachedData

    def process(self,datasource):
        data = self.__preProcessData(datasource)
        data = data.groupby(data.index).agg({InputColumns.PRICE:['min', 'max','mean'], InputColumns.VOLUME:'sum',
                                             InputColumns.BUY_VOL:'sum',InputColumns.SELL_VOL: 'sum'})
        print("*********************************Input Data********************************")
        print(data.shape[0])
        data = self.re_create(data)
        return data

    #Having problem with multi-level indexing in Pandas after aggregation, Don't really understand what it is meant to do
    #for now just recreate another dataframe
    def re_create(self, data):
        df = pd.DataFrame(dtype= float)
        df[str(OriginalColumn.PRICE_MAX)] = data[InputColumns.PRICE]['max'].values
        df[str(OriginalColumn.PRICE_MIN)] = data[InputColumns.PRICE]['min'].values
        df[str(OriginalColumn.PRICE_MEAN)] = data[InputColumns.PRICE]['mean'].values
        df[str(OriginalColumn.VOLUME)] = data[InputColumns.VOLUME]['sum'].values
        df[str(OriginalColumn.BUY_VOL)] = data[InputColumns.BUY_VOL]['sum'].values
        df[str(OriginalColumn.SELL_VOL)] = data[InputColumns.SELL_VOL]['sum'].values
        df.index = data.index.values
        df.index.name = str(OriginalColumn.TIME)
        return df