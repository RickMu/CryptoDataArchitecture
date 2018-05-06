from abc import abstractmethod
class IDataAccessor:
    def __init__(self,dataset):
        self._dataset = dataset

    @abstractmethod
    def getColumnNames(self):
        return

    @abstractmethod
    def read(self,key,length,TailUp= True):
        return
