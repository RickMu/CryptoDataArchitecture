from solution.DataConsumer.DataSetConsumer.RealTimeDataConsumer import RealTimeDataConsumer
from solution.DataSet.DataEntry.contracts.IDataEntry import IDataEntry


class OfflineDataConsumer(RealTimeDataConsumer):

    def __init__(self,processor, dataEntrance: IDataEntry):
        super().__init__(processor,dataEntrance)

    def consume(self, data):
        processedData = self._processor.process(data)
        self._dataEntrance.insert(processedData)

    def isReadyToConsume(self):
        return self._dataEntrance.readyToConsume()






