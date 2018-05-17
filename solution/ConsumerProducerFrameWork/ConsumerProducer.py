from abc import abstractmethod
from threading import Thread
import time
'''
To Use This:
Need to have a class firstly implement Collector

Then a consumer
'''
class Consumer:

    def __init__(self):
        self._isReadyToConsume = False
    def isReadyToConsume(self):
        return self._isReadyToConsume
    def _toggleConsumeState(self):
        if self._isReadyToConsume is False:
            self._isReadyToConsume = True
        else:
            self._isReadyToConsume = False

    @abstractmethod
    def consume(self,data):
        return

class Worker(Thread):
    def __init__(self, queue, consumer):
        Thread.__init__(self)
        self._queue = queue
        self._consumer = consumer
    def _getData(self):
        if self._queue.empty():
            return None
        return self._queue.get()

    def run(self):
        while True:
            if self._consumer.isReadyToConsume():
                data = self._getData()
                if data is not None:
                    self._consumer.consume(data)
            time.sleep(5)


class Collector(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self._queue = queue

    def _addToQueue(self,data):
        self._queue.put(data)
