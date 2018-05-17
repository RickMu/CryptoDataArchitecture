from solution.DataCollector.contracts.IDataProvider import IDataProvider

class CsvReader(IDataProvider):

    def __init__(self,sourcePath):
        self._sourcePath = sourcePath

    def addConsumers(self, consumer):
        super().addConsumers(consumer)

    def onDataObtained(self, data):
        super().onDataObtained(data)