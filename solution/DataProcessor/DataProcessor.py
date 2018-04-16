import pandas as pd
from DataObject.ComputedColumns import OriginalColumn

class DataProcessor:
    
    def __init__(self):
        self.__cachedData = pd.DataFrame()
        
    #Gets the last minute data, 
    #and returns all data before the last minute for correct aggregation
    def __preProcessData(self, datasource):
        lastestedTime= datasource.tail(1).index.values[0]
        datasource = self.__cachedData.append(datasource)
        data = datasource[datasource.index < lastestedTime]
        self.__cachedData = datasource[datasource.index >= lastestedTime]
        return data
    
    def getCachedData(self):
        return self.__cachedData

    def process(self,datasource):
        data = self.__preProcessData(datasource)
        
        data = data.groupby('time').agg({'price':['min', 'max','mean'], 'volume':'sum'})#, 'BuyVol':'sum','SellVol': 'sum'})
            
        data[str(OriginalColumn.PRICE_MAX)] = data['price']['max']
        data[str(OriginalColumn.PRICE_MIN)] = data['price']['min']
        data[str(OriginalColumn.PRICE_MEAN)] = data['price']['mean']
        
        return data
        
        