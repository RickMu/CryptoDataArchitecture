
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
        self._tempFix_ZeroValues = {}

    #Similar to function inside ColumnRule
    def _nameToIdentifier(self,tuples):
        return str(tuples[0]) + str(tuples[1])

    def addPlot(self,tuples):

        name =  self._nameToIdentifier(tuples)
        self._plots[str(name)] = self.graph.plot()

        if tuples[1] == "":
            self._tempFix_ZeroValues[str(name)] = 0
        else:
            self._tempFix_ZeroValues[str(name)] = tuples[1]
        print("Truncate Length: "+str(self._tempFix_ZeroValues[str(name)]))

    def _parseDataToXY(self,key):
        startPos = self._tempFix_ZeroValues[key]
        format = "%Y-%m-%dT%H:%M"
        x = self._data[key].index.values
        x = [datetime.datetime.strptime(i[:16],format) for i in x]

        t = [i.timetuple() for i in x]

        timeStamp = [int(time.mktime(i)) for i in t]

        xy = {
            'x': timeStamp[startPos:],
            'y': list(self._data[key].values)[startPos:]
        }

        return xy

    def plot(self):

        for key,v in self._plots.items():
            xy = self._parseDataToXY(key)
            v.setData(xy, symbol='o', symbolSize=1)

    def onDataUpdate(self, data):
        for key in self._plots.keys():
            self._data[key] = self._data[key].append(data[key], ignore_index=False)
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
