from queue import Queue
from solution.DataCollector.Schedular.Schedular import Schedular
from solution.DataCollector.Schedular.Tickers import Tickers
from solution.ConsumerProducerFrameWork.ConsumerProducer import Worker

class SchedularController():

    def __init__(self):
        self._queue = Queue()
        self._schedular = Schedular(self._queue)
        self._worker = None

    def setRequestConditions(self,coin,timespan):
        self._schedular.setRequestConditions(coin,timespan)
    def setDataSetEntry(self,entry):
        self._worker = Worker(queue=self._queue, consumer=entry)
    def start(self):
        self._schedular.start()
        self._worker.start()