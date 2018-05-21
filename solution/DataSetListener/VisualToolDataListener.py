from solution.DataSetListener.contracts.IDataSetListener import BaseDataSetListener
import pyqtgraph as pg


class VisualToolDataListener(BaseDataSetListener, pg.QtCore.QThread):
    newData = pg.QtCore.Signal(object)

    def __init__(self, client,tuples : list = []):
        pg.QtCore.QThread.__init__(self)
        super().__init__(client)
        if tuples == []:
            self._tuples = None
        else:
            self._tuples = tuples

    def onDataUpdate(self, event) -> None:
        data = {}
        if self._tuples is not None:
            for model in self._tuples:
                modelID = self._toIdentifier(model)
                data[modelID] = self._client.readFromTail(modelID, event)
        else:
            data = self._client.readAllData()
        self._consume(data)

    def _toIdentifier(self,tuple):
        return str(tuple[0])+str(tuple[1])

    def _consume(self, data):
        self.newData.emit(data)
