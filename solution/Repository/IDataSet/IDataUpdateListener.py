from abc import abstractmethod
class IDataUpdateListener:

    @abstractmethod
    def notify(self,key):
        return
