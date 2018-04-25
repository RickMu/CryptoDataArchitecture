from abc import abstractmethod
class IDataUpdateListener:

    @abstractmethod
    def onDataUpdate(self,updatedLength):
        return

class IDataUpdateSubject:

    @abstractmethod
    def addListeners(self,listener):
        return

    @abstractmethod
    def notify(self,updatedLength):
        return

class IDataUpdateHandler:

    def __init__(self, dataset, dataaccessor):
        self._dataset = dataset
        self._dataaccessor = dataaccessor

    @abstractmethod
    def updateDataSet(self,updatedLength,indicators):
        return
