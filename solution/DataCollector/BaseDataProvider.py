from threading import Thread

from solution.DataCollector.contracts.IDataProvider import IDataProvider


class BaseDataProvider(IDataProvider,Thread):

    def __init__(self):
        Thread.__init__(self)
        self.consumers = []

    def addConsumers(self,consumer):
        self.consumers.append(consumer)

    def onDataObtained(self, data):
        for consumer in self.consumers:
            consumer.consume(data)
