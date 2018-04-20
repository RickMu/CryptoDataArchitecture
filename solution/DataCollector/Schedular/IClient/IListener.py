from abc import abstractmethod
class IListener:
    @abstractmethod
    def callback(self,data):
        return