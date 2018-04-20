from abc import abstractmethod

class IApiBuilder:

    @abstractmethod
    def buildFetchRequest(self,ticker, timeSpan= None):
        return
