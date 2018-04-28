from queue import Queue

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from solution.ConsumerProducerFrameWork.ConsumerProducer import Worker
from solution.DataCollector.SchedularController import SchedularController
from solution.DataCollector.Schedular.Tickers import Tickers
from solution.DataObject.ComputedColumns import ComputedColumn
from solution.DataObject.ComputedColumns import OriginalColumn
from solution.DataSet.ComputedDataSet.ComputedDataSet import ComputedDataSet
from solution.DataSet.ComputedDataSet.ComputedDataUpdateHandler import ComputedDataUpdateHandler
from solution.DataSet.ComputedDataSet.DataSetController import DataSetController
from solution.DataSet.ComputedDataSet.TechnicalIndicatorsFactory import TechnicalIndicatorsFactory
from solution.DataSet.DataAccessor.DataSetAccessor import DataSetAccessor
from solution.Operators.Operator import OperatorType
from solution.VisualTools.DataCollector.GraphDataCollector import GraphDataCollector
from solution.VisualTools.DataUpdateContract.IDataUpdateContract import DataUpdateSubject
from solution.VisualTools.graph.Consumer import GraphDataConsumer
from solution.VisualTools.graph.customgraph import CustomGraph
from solution.DataSet.DataSetSystem import DataSetSystem


class PyQtWindowWrapper(DataUpdateSubject):
    def __init__(self,consumer):
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle("pyQTGRAPH: Tryout")
        self._listeners = []
        self._consumer= consumer
        self._consumer.toggleState()
        self._currow=0

    def start(self):
        import sys
        self._consumer.newData.connect(self.notify)
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def addGraph(self,g,rowspan=2,colspan=2):
        self.win.addItem(g.graph,self._currow,0,rowspan,colspan)
        self._currow+=rowspan
        self._addListener(g,)

    def _addListener(self,g):
        self._listeners.append(g)

    def notify(self,data):
        self._consumer.toggleState()
        for listener in self._listeners:
            listener.onDataUpdate(data)
        self._consumer.toggleState()


def createRequiredComponents(subjectDataAccessor):
    dataset = ComputedDataSet()
    dataAccessor = DataSetAccessor(dataset)
    updateHandler = ComputedDataUpdateHandler(dataset,subjectDataAccessor)
    indicatorFactory = TechnicalIndicatorsFactory()
    dataSetController = DataSetController(dataset,indicatorFactory,updateHandler)
    return dataSetController,dataAccessor

if __name__ == "__main__":
    system = DataSetSystem()
    system.initialize()
    system.addConfig(
        config= [
            (ComputedColumn.VOL_SUM, [(OriginalColumn.VOLUME, "")], OperatorType.SUM, 20),
            (ComputedColumn.MOMENTUM, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.DIFF, 20),
            (ComputedColumn.PRICE_AVG, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.MOVAVG, 20)
        ]
    ).addConfig(
        config=[
            (ComputedColumn.MOMENTUM_SUM, [(ComputedColumn.MOMENTUM, 20)], OperatorType.SUM, 20),
            (ComputedColumn.MOMENTUM_AVG, [(ComputedColumn.MOMENTUM, 20)], OperatorType.MOVAVG, 20)
        ]
    )

    schedular = SchedularController()
    schedular.setRequestConditions(coin=Tickers.BITCOIN, timespan=(0, 1))
    schedular.setDataSetEntry(system.getHeadDataSetController())
    schedular.start()

    consumer = GraphDataConsumer()
    app = PyQtWindowWrapper(consumer)
    queue = Queue()
    graphDataCollector = GraphDataCollector(queue, system.getDataAccessors())
    graphDataWorker = Worker(queue=queue, consumer=consumer)
    system.getTailDataSetController().addListeners(graphDataCollector)
    graphDataWorker.start()

    g1 = CustomGraph()
    g1.addPlot(OriginalColumn.VOLUME)

    g2 = CustomGraph()
    g2.addPlot(OriginalColumn.PRICE_MAX)
    g2.addPlot(OriginalColumn.PRICE_MEAN)
    app.addGraph(g1)
    app.addGraph(g2)
    app.start()