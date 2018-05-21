from solution.DataProcessor.DataSourceClient.contracts.IClient import IClient


class IDataSetListener:

    def onDataUpdate(self,event) -> None:
        pass

class BaseDataSetListener(IDataSetListener):

    def __init__(self, client : IClient):
        self._client = client

    def onDataUpdate(self, event) -> None:
        pass

