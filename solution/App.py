import sys

from solution.DataCollector.Schedular.Schedular import Schedular
from solution.DataConsumer.DataSetConsumer.RealTimeDataConsumer import RealTimeDataConsumer
from solution.DataProcessor.DataProcessor import DataProcessor
from solution.DataSetListener.VisualToolDataListener import VisualToolDataListener

sys.path.append("B:\\MyGit\\CryptoCoin")

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from solution.DataCollector.Schedular.Tickers import Tickers
from solution.DataObject.ComputedColumns import ComputedColumn
from solution.DataObject.ComputedColumns import OriginalColumn
from solution.Operators.Operator import OperatorType
from solution.VisualTools.DataUpdateContract.IDataUpdateContract import DataUpdateSubject
from solution.VisualTools.GraphBuilder import GraphBuilder
from solution.DataSet.DataSetSystem import DataSetSystem


class PyQtWindowWrapper(DataUpdateSubject):
    def __init__(self, consumer):
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle("pyQTGRAPH: Tryout")
        self._listeners = []
        self._consumer = consumer
        self._currow = 0

    def start(self):
        import sys
        self._consumer.newData.connect(self.notify)
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def addGraph(self, g, rowspan=2, colspan=2):
        self.win.addItem(g.graph, self._currow, 0, rowspan, colspan)
        self._currow += rowspan
        self._addListener(g, )

    def _addListener(self, g):
        self._listeners.append(g)

    def notify(self, data):
        for listener in self._listeners:
            listener.onDataUpdate(data)


if __name__ == "__main__":
    '''
       Note: All rows of data are minutely aggregated data 
       Cached data are data that is not aggregated minutely yet, 
       because the minute has not gone past, and so it's not sent to the dataset
       what is printed on the commandline are row counts

       DataSetSystem:
       Each time config is added, a new dataset with those columns are created and it sits at the bottom of the
       hierachy. Data obtained from worker notifies data handlers each dataset has from from top to bottom.

       '''

    DAY = 1440
    HOURS_5 = 300
    system = DataSetSystem()
    system.initialize()
    system.addConfig(
        config=[
            (
            ComputedColumn.BINARISE_PRICE, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.BINARISE_LEFT_DIFF, HOURS_5),
            (ComputedColumn.BINARISE_PRICE, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.BINARISE_LEFT_DIFF, 2),
            (ComputedColumn.ALIGN_VOLUME_SUM_PRICE, [(OriginalColumn.VOLUME, ""), (OriginalColumn.PRICE_MEAN, "")],
             OperatorType.SUM_ALIGN_CHANGE, DAY),
            (ComputedColumn.VOL_SUM, [(OriginalColumn.VOLUME, "")], OperatorType.SUM, DAY),
            (ComputedColumn.MOMENTUM, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.DIFF, HOURS_5),
            (ComputedColumn.MOMENTUM, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.DIFF, DAY),
            (ComputedColumn.PRICE_AVG, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.MOVAVG, HOURS_5),
            (ComputedColumn.BUY_MINUS_SELL, [(OriginalColumn.BUY_VOL, ""), (OriginalColumn.SELL_VOL, "")],
             OperatorType.SUBTRACT, 0),
            (ComputedColumn.PRICE_STOK, [(OriginalColumn.PRICE_MEAN, "")
                , (OriginalColumn.PRICE_MAX, "")
                , (OriginalColumn.PRICE_MIN, "")], OperatorType.STOK, HOURS_5),
            (ComputedColumn.AROON_UP_PRICE, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.AROON_UP, DAY),
            (ComputedColumn.AROON_DOWN_PRICE, [(OriginalColumn.PRICE_MEAN, "")], OperatorType.AROON_DOWN, DAY),
        ]
    ).addConfig(
        config=[
            (ComputedColumn.ALIGN_VOLUME_SUM_PRICE, [(OriginalColumn.VOLUME, ""), (ComputedColumn.BINARISE_PRICE, 2)],
             OperatorType.SUM_ALIGN_CHANGE, DAY),
            (ComputedColumn.MOMENTUM_AVG, [(ComputedColumn.MOMENTUM, HOURS_5)], OperatorType.MOVAVG, HOURS_5),
            (ComputedColumn.MOMENTUM_VOL, [(ComputedColumn.MOMENTUM, HOURS_5), (ComputedColumn.VOL_SUM, DAY)],
             OperatorType.MULTIPLY, 0),
            (ComputedColumn.WILLR_VOL, [
                (ComputedColumn.VOL_SUM, DAY),
                (ComputedColumn.VOL_SUM, DAY),
                (ComputedColumn.VOL_SUM, DAY)], OperatorType.STOK, HOURS_5),
            (ComputedColumn.BUY_MINUS_SELL_VOL_SUM, [(ComputedColumn.BUY_MINUS_SELL, "")], OperatorType.SUM, DAY),
        ]
    ).addConfig(
        config=[
            (ComputedColumn.STOK_MOMENTUM_VOL, [(ComputedColumn.MOMENTUM_VOL, "")
                , (ComputedColumn.MOMENTUM_VOL, "")
                , (ComputedColumn.MOMENTUM_VOL, "")], OperatorType.STOK, DAY),
            (ComputedColumn.WILLR_BUY_MINUS_SELL, [(ComputedColumn.BUY_MINUS_SELL_VOL_SUM, DAY),
                                                   (ComputedColumn.BUY_MINUS_SELL_VOL_SUM, DAY),
                                                   (ComputedColumn.BUY_MINUS_SELL_VOL_SUM, DAY)], OperatorType.STOK,
             HOURS_5)
            , (ComputedColumn.BUY_SELL_SUM_DIFF, [(ComputedColumn.BUY_MINUS_SELL_VOL_SUM, DAY)], OperatorType.DIFF, DAY)
            , (ComputedColumn.STOK_ALIGN_VOLUME_SUM_PRICE, [(ComputedColumn.ALIGN_VOLUME_SUM_PRICE, DAY)
                , (ComputedColumn.ALIGN_VOLUME_SUM_PRICE, DAY)
                , (ComputedColumn.ALIGN_VOLUME_SUM_PRICE, DAY)], OperatorType.STOK, DAY)
        ]
    ).addConfig(
        config=[
            (ComputedColumn.MOMENTUM_CROSS_BUY_SELL_SUM_DIFF, [(ComputedColumn.BUY_SELL_SUM_DIFF, DAY)
                , (ComputedColumn.MOMENTUM, HOURS_5)], OperatorType.MULTIPLY, 0)
        ]
    )

    '''
    processor = DataProcessor()
    dataConsumer = OfflineDataConsumer(processor, system.getHeadDataSetController())
    dataProvider = JsonReader("B:\\MyGit\\Acx-API\\Dataset\\bitcoin.json" ,dataConsumer)
    dataProvider.start()
    '''

    processor = DataProcessor()
    dataConsumer = RealTimeDataConsumer(processor, system.getClient())
    dataConsumer.start()

    schlr = Schedular()
    schlr.addConsumers(dataConsumer)
    schlr.setRequestConditions(Tickers.BITCOIN, (2, 1))
    schlr.start()

    consumer = VisualToolDataListener(system.getClient())
    app = PyQtWindowWrapper(consumer)
    system.getClient().addAdditionalSystem(consumer)

    grapher = GraphBuilder()

    grapher.addGraph() \
        .addPlot((ComputedColumn.PRICE_AVG, HOURS_5)) \
        .addPlot((OriginalColumn.PRICE_MEAN, "")) \
        .addGraph() \
        .addPlot((ComputedColumn.PRICE_STOK, HOURS_5)) \
        .addGraph() \
        .addPlot((ComputedColumn.VOL_SUM, DAY)) \
        .addGraph() \
        .addPlot((ComputedColumn.WILLR_VOL, HOURS_5)) \
        .addGraph() \
        .addPlot((ComputedColumn.BUY_MINUS_SELL_VOL_SUM, DAY)) \
        .addGraph() \
        .addPlot((ComputedColumn.WILLR_BUY_MINUS_SELL, HOURS_5)) \
        .addGraph() \
        .addPlot((ComputedColumn.MOMENTUM_VOL, "")) \
        .addGraph() \
        .addPlot((ComputedColumn.STOK_MOMENTUM_VOL, DAY)) \
        .addGraph() \
        .addPlot((ComputedColumn.AROON_UP_PRICE, DAY), symbol_brush='g') \
        .addPlot((ComputedColumn.AROON_DOWN_PRICE, DAY), symbol_brush='r') \
        .addGraph() \
        .addPlot((ComputedColumn.ALIGN_VOLUME_SUM_PRICE, DAY)) \
        .addGraph() \
        .addPlot((ComputedColumn.STOK_ALIGN_VOLUME_SUM_PRICE, DAY))

    '''

    .addGraph()\
        .addPlot((ComputedColumn.MOMENTUM_BUY_MINUS_SELL_VOL_SUM,""))\
    .addGraph()\
        .addPlot((ComputedColumn.WILLR_MOMENTUM_BUY_MINUS_SELL_VOL_SUM,DAY))\
    '''
    grapher.Graph(app)
    app.start()
