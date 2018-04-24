from solution.Repository.IDataSet.IDataSet import IDataSet
import pandas as pd
from collections import defaultdict
from threading import Lock

class ComputedDataSet(IDataSet):

    def __init__(self):
        self._columns = defaultdict(pd.Series)
        self._locks = defaultdict(Lock)

    def addColumn(self,name):
        self._locks[name] = Lock()
        self._columns[name] = pd.Series()

    def updateColumn(self,key,data):
        self.__checkColumnExist(key)
        self._locks[key].acquire()
        self._columns[key]=self._columns[key].append(data,ignore_index=False)
        print("*****************Updates of %s****************" %(key))
        print(self._columns[key].shape[0])
        self._locks[key].release()

    #Method not implemented and shouldn't be called
    def updateColumns(self, data):
        super().updateColumns(data)
        raise Exception("Unimplemented Method")

    def getColumn(self,name):
        return self._columns[name]

    def getColumnNames(self):
        return self._columns.keys()

    def __checkColumnExist(self,name):
        if name not in self._columns.keys():
            raise Exception("Column name %s not in %s: " % (name,self._columns.keys()))
