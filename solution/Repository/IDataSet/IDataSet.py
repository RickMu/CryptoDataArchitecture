from abc import abstractmethod


class IDataSet:


    @abstractmethod
    def read(self,key):
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
    def readAll(self):
        return

    @abstractmethod
    def addUpdateListener(self, listener):
        return

    @abstractmethod
    def notify(self,updatedLength,key):
        return
