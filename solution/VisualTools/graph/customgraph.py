
from solution.VisualTools.DataUpdateContract.IDataUpdateContract import DataUpdateListener
from solution.VisualTools.graph.Axis import CustomDateAxis
import pyqtgraph as pg
from collections import defaultdict
import datetime
import pandas as pd
import time

class CustomGraph(DataUpdateListener):
    def __init__(self):
        self._axis = CustomDateAxis(orientation='bottom')
        self.graph = pg.PlotItem( axisItems={'bottom': self._axis})
        self._plots = {}
        self._data = defaultdict(pd.Series)

    def addPlot(self,name):
        self._plots[str(name)] = self.graph.plot()

    def _parseDataToXY(self,key):

        format = "%Y-%m-%dT%H:%M"
        x = self._data[key].index.values
        x = [datetime.datetime.strptime(i[:16],format) for i in x]

        t = [i.timetuple() for i in x]

        timeStamp = [int(time.mktime(i)) for i in t]

        xy = {
            'x': timeStamp,
            'y': list(self._data[key].values)
        }
        print(xy)
        return xy

    def plot(self):

        for key,v in self._plots.items():
            xy = self._parseDataToXY(key)
            v.setData(xy, symbol='o', symbolSize=1)

    def onDataUpdate(self, data):
        for key in self._plots.keys():
            self._data[key] = self._data[key].append(data[key], ignore_index=False)
            print(self._data[key])
        self.plot()

'''
For some reason it doesn't work in this file
from pyqtgraph.Qt import QtCore, QtGui

class PyQtWindow:
    def __init__(self):
        self.win = pg.GraphicsWindow()

    def start(self):
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def addGraph(self,g):
        self.win.addItem(g.graph)
'''


if __name__ == "__main__":

    g = CustomGraph("test", "test")
    g.addPlot("Name")
    app = PyQtWindow()
    app.addGraph(g)
