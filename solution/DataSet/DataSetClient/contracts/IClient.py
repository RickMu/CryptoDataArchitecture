from abc import abstractmethod

class IClient:

    def insert(self,data):
        return

    def read(self,colName):
        return

    def readyToConsume(self):
        return