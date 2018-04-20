from abc import abstractmethod
class IClient:

    def __init__(self):
        self._returnedData = None

    @abstractmethod
    #Most api calls wouldn't support a timespan, but the ec2 we have does
    def fetchData(self,ticker, timeSpan = None):
        return

    @abstractmethod
    def setRequestConditions(self,ticker, timeSpan = None):
        return

    def getReturnedData(self):
        return self._returnedData

