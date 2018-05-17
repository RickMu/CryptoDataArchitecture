
'''
Meant as a main controller for the whole system
'''

from solution.DataSet.ComputedDataSet.ComputedDataSet import ComputedDataSet
from solution.DataSet.OriginalDataSet.DataSet import DataSet
from solution.DataSet.DataAccessor.DataSetAccessor import DataSetAccessor
from solution.DataProcessor.DataProcessor import DataProcessor
from solution.DataSet.ComputedDataSet.DataSetController import DataSetController
from solution.DataSet.ComputedDataSet.ComputedDataUpdateHandler import ComputedDataUpdateHandler
from solution.DataSet.ComputedDataSet.TechnicalIndicatorsFactory import TechnicalIndicatorsFactory


class DataSetSystem:

    def __init__(self):
        self._configs=[]
        self._dataaccessors=[]
        self._dataSetControllers=[]

    def getHeadDataSetController(self):
        return self._dataSetControllers[0]

    def getTailDataSetController(self):
        return self._dataSetControllers[-1]

    def getDataAccessors(self):
        return self._dataaccessors

    def initialize(self):
        processor = DataProcessor()
        dataSet = DataSet(processor)
        accessor = DataSetAccessor(dataSet)
        self._dataSetControllers.append(dataSet)
        self._dataaccessors.append(accessor)

    def addConfig(self,config):
        dc, da = self._createDataSetControllerAndAccessor(self._dataaccessors[-1])
        dc.initialize(config)
        self._dataSetControllers[-1].addListeners(dc)
        self._dataSetControllers.append(dc)
        self._dataaccessors.append(da)
        return self

    def _createDataSetControllerAndAccessor(self,subjectDataAccessor):
        dataset = ComputedDataSet()
        dataAccessor = DataSetAccessor(dataset,subjectDataAccessor)
        updateHandler = ComputedDataUpdateHandler(dataset, subjectDataAccessor)
        indicatorFactory = TechnicalIndicatorsFactory()
        dataSetController = DataSetController(dataset, indicatorFactory, updateHandler)
        return dataSetController, dataAccessor