from abc import abstractmethod

class IProcessor:

    @abstractmethod
    def process(self,data):
        return