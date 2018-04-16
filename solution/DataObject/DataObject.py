
from abc import ABC, abstractmethod
class OnDataChangeListener:
    
    @abstractmethod
    def onDataChange(self,additionalData):
        return
      

class DataObject(OnDataChangeListener):
    
    def __init__(self,identifier, data,mediator):
        self._identifier = identifier
        self._data = data
        self._mediator = mediator
    def getName(self):
        return str(self._identifier)
    def getIdentifier(self):
        return self._identifier
    def getData(self):
        return self._data.read(self.getName())   
