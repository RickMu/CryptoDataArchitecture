from abc import abstractmethod


class IDataSet:
    @abstractmethod
    def getColumn(self,name):
        return

    @abstractmethod
    def updateColumn(self,key,data):
        return

    @abstractmethod
    def updateColumns(self,data):
        return

    @abstractmethod
    def getColumnNames(self):
        return

    @abstractmethod
    def addUpdateListener(self, listener):
        return

    @abstractmethod
    def notify(self,updatedLength):
        return
