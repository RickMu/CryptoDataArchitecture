from solution.ConsumerProducerFrameWork.ConsumerProducer import Collector
from solution.Contracts.IDataUpdateContracts import IDataUpdateListener,IDataUpdateHandler
'''
ToDo:
Need to make data changes just a state change and data sorted by ids
'''
class DataCollector(Collector, IDataUpdateListener,IDataUpdateHandler):

    def __init__(self,queue,dataaccessors):
        Collector.__init__(self,queue)
        self._accessors = dataaccessors

    def run(self):
        return

    def onDataUpdate(self, event):
        data= {}

        for accessor in self._accessors:
            cols = accessor.getColumnNames()
            for col in cols:
                result = accessor.read(cols, event)
                data[col] = result
        self._addToQueue(data)





