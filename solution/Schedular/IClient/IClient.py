from abc import abstractmethod
class IClient:

    def __init__(self,listener):
        self._listener = listener

    @abstractmethod
    def fetchData(self,ticker):
        return
