
'''
Meant as a main controller for the whole system
'''
from solution.ConsumerProducerFrameWork.ConsumerProducer import Worker
from solution.DataCollector.Schedular.Schedular import Schedular

from solution.DataCollector.Schedular.Tickers import Tickers
from solution.DataObject.ComputedColumns import OriginalColumn
from solution.DataSet.ComputedDataSet.ComputedDataSet import ComputedDataSet
from solution.DataSet.OriginalDataSet.DataSet import DataSet
from solution.DataSet.DataAccessor.DataAccessor import DataAccessor
from solution.DataSet.DataProcessor.DataProcessor import DataProcessor
from solution.DataSet.ComputedDataSet.DataSetManager import DataSetManager
from solution.DataSet.ComputedDataSet.ComputedDataUpdateHandler import ComputedDataUpdateHandler
from solution.DataSet.ComputedDataSet.TechnicalIndicatorsFactory import TechnicalIndicatorsFactory
from solution.Operators.Operator import OperatorType
from solution.DataObject.ComputedColumns import ComputedColumn
from solution.VisualTools.DataCollector.GraphDataCollector import GraphDataCollector
from queue import Queue
from solution.VisualTools.graph.customgraph import CustomGraph

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
        accessor = DataAccessor(dataSet)
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
        dataSetController = DataSetManager(subjectDataAccessor)

        return dataSetController, dataSetController.getDataAccessor()