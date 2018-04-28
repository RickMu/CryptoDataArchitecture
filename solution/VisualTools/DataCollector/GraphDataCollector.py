from solution.ConsumerProducerFrameWork.ConsumerProducer import Collector
from solution.Contracts.IDataUpdateContracts import IDataUpdateListener

class GraphDataCollector(Collector, IDataUpdateListener):

    def __init__(self,queue,dataccessors):
        Collector.__init__(self,queue)
        self._accessors = dataccessors

    def onDataUpdate(self, event):
        data = {}
        for accessor in self._accessors:
            for col in accessor.getColumnNames():
                data[col] = accessor.read(col,event)
        self._addToQueue(data)

