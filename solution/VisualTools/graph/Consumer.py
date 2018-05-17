from solution.ConsumerProducerFrameWork.ConsumerProducer import Consumer
import pyqtgraph as pg

class GraphDataConsumer(Consumer, pg.QtCore.QThread):
    newData = pg.QtCore.Signal(object)
    def __init__(self):
        pg.QtCore.QThread.__init__(self)
        Consumer.__init__(self)

    def toggleState(self):
        self._toggleConsumeState()

    def consume(self, data):
        self.newData.emit(data)
