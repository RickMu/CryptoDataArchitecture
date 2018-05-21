import pandas as pd

from solution.DataProcessor.DataSourceClient.contracts.IClient import IClient
from solution.DataSet.ComputedDataSet.DataSetManager import DataSetManager
from solution.DataSet.DataAccessor.DataAccessor import DataAccessor
from solution.DataSet.DataEntry.DataEntry import DataEntry


class DataSetClient(IClient):
    def __init__(self,bottomDataAccessor: DataAccessor, dataEntrance: DataEntry, lastDataManager: DataSetManager):
        self._dataAccessor = bottomDataAccessor
        self._dataEntry = dataEntrance
        self._lastDataSetManager = lastDataManager

    def insert(self, data) -> None:
        self._dataEntry.insert(data)

    def readyToConsume(self) -> bool:
        return self._dataEntry.readyToConsume()

    def read(self, key) -> pd.Series:
        return self._dataAccessor.read(key)

    #This should just be a temp solution
    def readAllData(self) -> dict:
        dct = {}
        accessor = self._dataAccessor
        while accessor is not None:
            for col in accessor.getColumnNames():
                dct[col] = accessor.read(col)
            accessor = accessor.parent
        return dct

    def readFromTail(self, key, length) -> pd.Series:
        return self._dataAccessor.readPartial(key,length)

    def addAdditionalSystem(self, additionalSystem) -> None:
        self._lastDataSetManager.addListeners(additionalSystem)

