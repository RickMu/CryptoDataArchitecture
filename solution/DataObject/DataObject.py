
from abc import ABC, abstractmethod
class OnDataChangeListener:
    
    @abstractmethod
    def onDataChange(self,additionalData):
        return
      

class DataObject(OnDataChangeListener):
    
    def __init__(self,identifier, data):
        self.__identifier = identifier
        self.__data = data
    def getName(self):
        return str(self.__identifier[0])+str(self.__identifier[1])
    def getIdentifier(self):
        return self.__identifier
    def getData(self):
        return self.__data   
    def onDataChange(self, requiredData, updatedLength):
        return
        

class DataObjectFactory():
    def __init__(self,dataset):
        self.__dataset = dataset
        self.__objects = []
        
    def __createOriginalObjects(self):
        for name in self.__dataset.OriginalKeys():
            dO = DataObject(name, self.__dataset)
            self.__objects.append(dO)

    