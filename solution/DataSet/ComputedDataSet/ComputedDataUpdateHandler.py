from solution.DataSet.IDataSet.IDataUpdateListener import IDataUpdateHandler
from collections import defaultdict
import pandas as pd
from threading import Thread
class ComputedDataUpdateHandler(IDataUpdateHandler):
    def __init__(self,dataset, dataaccessor):
        IDataUpdateHandler.__init__(self,dataset, dataaccessor)

    def _updateColumn(self,rule,updatedLength,requiredData):
        data = rule.compute(requiredData, updatedLength)
        self._dataset.updateColumn(rule.getIdentifier(), data)

    def _getRequiredData(self, indicator, updatedLength):
        rqCols = indicator.getRequiredColumns()
        data = defaultdict(pd.Series)
        for col in rqCols:
            data[col] = self._dataaccessor.read(col, updatedLength + indicator.getPeriods())
        return data
        # Needs Checking
    def _updateDataSet(self,updatedLength, indicator):
        requiredData = self._getRequiredData(indicator,updatedLength)
        self._updateColumn(indicator,updatedLength,requiredData)

    def updateDataSet(self, updatedLength,indicators):
        threads = []
        for indicator in indicators:
            t = Thread(target=self._updateDataSet, args=(updatedLength, indicator))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()






