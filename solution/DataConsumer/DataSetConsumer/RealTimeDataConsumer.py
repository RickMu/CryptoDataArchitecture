
from abc import abstractmethod

from solution.DataConsumer.contracts.IDataConsumer import IDataConsumer
from threading import Thread
from queue import Queue
import time

from solution.DataSet.DataEntry.contracts.IDataEntry import IDataEntry


class RealTimeDataConsumer(IDataConsumer, Thread):

    def __init__(self, processor, dataEntrance:IDataEntry):
        Thread.__init__(self)
        self._processor = processor
        self._dataEntrance = dataEntrance
        self._processedData = Queue()

    def consume(self, data):
        processedData = self._processor.process(data)
        if not processedData is None:
            self._processedData.put(processedData)

    def run(self) -> None:
        while True:
            if not self._processedData.empty()and self._dataEntrance.readyToConsume():
                self._dataEntrance.insert(self._processedData.get())
            time.sleep(5)