from solution.DataSet.DataSetClient.contracts.IClient import IClient

class Client(IClient):

    def __init__(self,headDataSet):
        self._headDataSet = headDataSet
        self._readyToConsume = True

    def notify(self):
        super().notify()

    def addListener(self):
        super().addListener()

    def insert(self, data):
        self._toggleConsumeState()
        self._headDataSet.consume(data)
        self._toggleConsumeState()

    def _toggleConsumeState(self):
        self._readyToConsume = not self._readyToConsume

    def read(self, colName):
        super().read(colName)

    def readyToConsume(self):
        super().readyToConsume()