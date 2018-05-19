from solution.DataSet.DataSetClient.contracts.IClient import IClient

class Client(IClient):

    def __init__(self,headDataSet):
        self._headDataSet = headDataSet
        self._readyToConsume = True

    def insert(self, data):
        if type(data) is not dict:
            raise Exception("Data to inject in data base need to be a dictionary")
        self._toggleConsumeState()
        for k,v in data.items():
            self._headDataSet.addColumn(k)
            self._headDataSet.updateColumn(k,v)
        self._toggleConsumeState()

    def _toggleConsumeState(self):
        self._readyToConsume = not self._readyToConsume

    def read(self, colName):
        super().read(colName)

    def readyToConsume(self):
        return self._readyToConsume