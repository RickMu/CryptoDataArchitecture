from abc import abstractmethod

class IDataProvider:

    @abstractmethod
    def addConsumers(self,consumer):
        return

    @abstractmethod
    def onDataObtained(self,data):
        return
