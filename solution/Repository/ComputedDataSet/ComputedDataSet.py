from solution.Repository.IDataSet.IDataSet import IDataSet
import pandas as pd
from collections import defaultdict
from threading import Lock

class ComputedDataSet(IDataSet):

    def __init__(self):
        self._columns = defaultdict(pd.Series)
        self._locks = defaultdict(Lock)
        self.__listener = None

    def __addColumn(self,name):
        self._locks[name] = Lock()
        self._columns[name] = pd.Series()

    def __checkColumnExist(self,name):
        if name not in self._columns.keys():
            raise Exception("Column name %s not in %s: " % (name,self._columns.keys()))
    def updateColumn(self,key,data):
        self.__checkColumnExist(key)
        self._locks[key].acquire()

        self._columns[key].append(data,ignore_index=False)
        self.notify(data.shape[0],key)

        self._locks[key].release()

    def addUpdateListener(self,listener):
        self.__listener = listener

    def notify(self,updatedlength,key):
        if self.__listener is None:
            return
        self.__listener.notify(updatedlength,key)

    def readAll(self):
        return self._columns

    def read(self, key):
        return self._columns[key]

    #Method not implemented and shouldn't be called
    def updateColumns(self, data):
        super().updateColumns(data)
        raise Exception("Unimplemented Method")

    def getColumnNames(self):
        self._columns.keys()
