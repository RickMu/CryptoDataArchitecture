from solution.Contracts.IDataUpdateContracts import IDataUpdateListener,IDataUpdateSubject
'''
Not Cleanly designed:
Rule Set handles two responsibilities: Creation of rules and, also act as an updater
'''

class DataSetController(IDataUpdateListener,IDataUpdateSubject):
    def __init__(self,dataset,technicalIndicatorsFactory, dataUpdateHandler):
        self._indicators = []
        self._dataset = dataset
        self._factory = technicalIndicatorsFactory
        self._listener = []
        self._dataUpdateHandler = dataUpdateHandler

    def addListeners(self,listener):
        self._listener.append(listener)
    def notify(self, event):
        for listener in self._listener:
            listener.onDataUpdate(event)

    def onDataUpdate(self, event):
        self._dataUpdateHandler.updateDataSet(event, self._indicators)
        self.notify(event)

    def initialize(self, configs):
        indicators = self._factory.create(configs)
        for i in indicators:
            self._dataset.addColumn(i.getIdentifier())
        self._indicators = indicators




