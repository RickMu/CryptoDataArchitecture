from abc import abstractmethod
class IDataAccessor:
    def __init__(self,dataset,parent = None):
        self.parent = parent
        self._dataset = dataset

    @abstractmethod
    def getColumnNames(self):
        return

    @abstractmethod
    def read(self,key,length,TailUp= True):
        return
