from solution.DataConsumer.contracts.IDataConsumer import IDataConsumer
from queue import Queue
from threading import Thread
import time

class RawDataConsumer(IDataConsumer, Thread):

    def __init__(self, client, processor):
        Thread.__init__(self)
        self._client = client
        self._processor = processor
        self._processedData = Queue()

    def consume(self, data):
        processedData = self._processor.process(data)
        if not processedData is None:
            self._processedData.put(processedData)

    def run(self):

        while not self._processedData.empty():
            if self._client.readyToConsume():
                self._client.insert(self._processedData.get())
            time.sleep(5)
