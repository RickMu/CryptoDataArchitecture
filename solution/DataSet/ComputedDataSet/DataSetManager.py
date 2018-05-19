from solution.Contracts.IDataUpdateContracts import IDataUpdateListener,IDataUpdateSubject
from solution.DataSet.ComputedDataSet.ComputedDataSet import ComputedDataSet
from solution.DataSet.ComputedDataSet.ComputedDataUpdateHandler import ComputedDataUpdateHandler
from solution.DataSet.ComputedDataSet.TechnicalIndicatorsFactory import TechnicalIndicatorsFactory
from solution.DataSet.DataAccessor.DataAccessor import DataAccessor

'''
Not Cleanly designed:
Rule Set handles two responsibilities: Creation of rules and, also act as an updater
'''

class DataSetManager(IDataUpdateListener, IDataUpdateSubject):
    def __init__(self, parentDataAccessor):
        self._indicators = []
        self._listener = []
        self._dataset = ComputedDataSet()
        self._dataUpdateHandler = ComputedDataUpdateHandler(self._dataset,parentDataAccessor)
        self._dataAccessor = DataAccessor(self._dataset,parentDataAccessor)

    def getDataAccessor(self):
        return self._dataAccessor

    def initialize(self, configs):
        indicators = TechnicalIndicatorsFactory().create(configs)
        for i in indicators:
            self._dataset.addColumn(i.getIdentifier())
        self._indicators = indicators

    def addListeners(self,listener):
        self._listener.append(listener)
    def notify(self, event):
        for listener in self._listener:
            listener.onDataUpdate(event)

    def onDataUpdate(self, event):
        self._dataUpdateHandler.updateDataSet(event, self._indicators)
        self.notify(event)



