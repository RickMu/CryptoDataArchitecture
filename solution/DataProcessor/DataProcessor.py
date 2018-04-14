import pandas as pd

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
            
        data['PriceMax'] = data['price']['max']
        data['PriceMin'] = data['price']['min']
        data['PriceMean'] = data['price']['mean']
        
        return data
        
        