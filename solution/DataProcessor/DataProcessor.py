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
        data.index.name = str(OriginalColumn.TIME)
        print("*********************************Input Data********************************")
        print(data.shape[0])
        data = self.dataFrameToDict(data)

        return data

    #Having problem with multi-level indexing in Pandas after aggregation, Don't really understand what it is meant to do
    #for now just recreate another dataframe
    def dataFrameToDict(self, data):
        dct = {}
        dct[str(OriginalColumn.PRICE_MAX)] = data[InputColumns.PRICE]['max']
        dct[str(OriginalColumn.PRICE_MIN)] = data[InputColumns.PRICE]['min']
        dct[str(OriginalColumn.PRICE_MEAN)] = data[InputColumns.PRICE]['mean']
        dct[str(OriginalColumn.VOLUME)] = data[InputColumns.VOLUME]['sum']
        dct[str(OriginalColumn.BUY_VOL)] = data[InputColumns.BUY_VOL]['sum']
        dct[str(OriginalColumn.SELL_VOL)] = data[InputColumns.SELL_VOL]['sum']

        return dct