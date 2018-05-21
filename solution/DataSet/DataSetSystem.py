'''
Meant as a main controller for the whole system
'''

from solution.DataProcessor.DataProcessor import DataProcessor
from solution.DataProcessor.DataSourceClient.DataSetClient import DataSetClient
from solution.DataSet.ComputedDataSet.ComputedDataSet import ComputedDataSet
from solution.DataSet.ComputedDataSet.DataSetManager import DataSetManager
from solution.DataSet.DataAccessor.DataAccessor import DataAccessor
from solution.DataSet.DataEntry.DataEntry import DataEntry


class DataSetSystem:

    def __init__(self):
        self._configs = []
        self._dataaccessors = []
        self._dataSetControllers = []
        self._client: DataAccessor = None

    def getHeadDataSetController(self):
        return self._dataSetControllers[0]

    def getTailDataSetController(self):
        return self._dataSetControllers[-1]

    def getDataAccessors(self):
        return self._dataaccessors

    def getTailDataAccessor(self) -> DataAccessor:
        return self._dataaccessors[-1]

    def initialize(self, ):
        ds = ComputedDataSet()
        client = DataEntry(ds)
        accessor = DataAccessor(ds)
        self._dataSetControllers.append(client)
        self._dataaccessors.append(accessor)

    def addConfig(self, config):
        dc, da = self._createDataSetControllerAndAccessor(self._dataaccessors[-1])
        dc.initialize(config)
        self._dataSetControllers[-1].addListeners(dc)
        self._dataSetControllers.append(dc)
        self._dataaccessors.append(da)
        return self

    def _createDataSetControllerAndAccessor(self, subjectDataAccessor):
        dataSetController = DataSetManager(subjectDataAccessor)
        return dataSetController, dataSetController.getDataAccessor()

    def getClient(self):
        if self._client is None:
            self._client = DataSetClient(self.getTailDataAccessor(),self.getHeadDataSetController(), self.getTailDataSetController())
        return self._client
