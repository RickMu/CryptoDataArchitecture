from solution.Contracts.IDataUpdateContracts import IDataUpdateSubject

from solution.DataSet.DataEntry.contracts.IDataEntry import IDataEntry


class DataEntry(IDataEntry,IDataUpdateSubject):

    def __init__(self,headDataSet):
        self._headDataSet = headDataSet
        self._readyToConsume = True
        self._listeners = []

    def insert(self, data):
        if type(data) is not dict:
            raise Exception("Data to inject in data base need to be a dictionary")
        self._toggleConsumeState()
        length = 0

        for k,v in data.items():
            self._headDataSet.addColumn(k)
            self._headDataSet.updateColumn(k,v)
            length = v.size

        self.notify(length)
        self._toggleConsumeState()

    def _toggleConsumeState(self):
        self._readyToConsume = not self._readyToConsume

    def readyToConsume(self):
        return self._readyToConsume

    def addListeners(self, listener):
        self._listeners.append(listener)

    def notify(self, event):
        for listener in self._listeners:
            listener.onDataUpdate(event)