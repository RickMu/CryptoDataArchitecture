from abc import abstractmethod

class IClient:

    def notify(self):
        return

    def addListener(self):
        return

    def insert(self,data):
        return

    def read(self,colName):
        return

    def readyToConsume(self):
        return