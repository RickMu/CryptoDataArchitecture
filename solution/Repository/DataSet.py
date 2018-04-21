import pandas as pd
from threading import Lock, Thread
from collections import defaultdict
from solution.DataCollector.Worker.WorkableState import Consumer


class DataSet(Consumer):
    
    def __init__(self, processor, mediator):
        Consumer.__init__(self)
        self.__originalDF = pd.DataFrame(dtype=float)
        self.__uncompressedDF = pd.DataFrame(dtype=float)
        self.__computedDF = defaultdict(pd.Series)
        self.__computedLock = defaultdict(Lock)
        self.__datalock = Lock()
        self.__originalColumnListeners = []
        self.__computedColumnListeners = defaultdict(list)
        self.__dataProcessor = processor
        self.__mediator = mediator
        self.__mediator.setDataSet(self)
        super()._toggleState()
        
    def getSize(self):
        return self.__originalDF.shape[0]
    
    def getOriginalKeys(self):
        return self.__originalDF.keys()
    
    def getComputedKeys(self):
        return self.__computedDF.keys()

    def consume(self,data):
        self.updateOriginal(data)

    def updateOriginal(self,additionalData):
        self.__datalock.acquire()
        super()._toggleState()

        data = self.__dataProcessor.process(additionalData)
        print(data)
        self.__originalDF = self.__originalDF.append(data)
        self.__mediator.send('Original', data.shape[0])

        print(self.__originalDF)
        super()._toggleState()
        self.__datalock.release()
    #method should be retired
    def getAllData(self):
        return self.__originalDF
    def read(self,key):
        key = str(key)
        return self.readTail(key)
        # log it or print?
    
    def readTail(self,key, count = None):
        data= None
        key = str(key)
        if key in self.__originalDF.keys():
            data = self.__originalDF[key].values
        if key in self.__computedDF.keys():
            data = self.__computedDF[key].values
        if data is None:
            raise Exception("No specified key in \n%s \n%s" % (self.__originalDF.keys(), self.__computedDF.keys()))
       
        if count is not None:
            start = data.shape[0]-count
            if start <0:
                start = 0
            data = data[start:]
        return data
        
    def registerComputedColumn(self, computedColumnName):
        self.__computedDF[computedColumnName] = pd.Series()
        self.__computedLock[computedColumnName] = Lock()
    
    def updateComputedColumns(self,key,additionalData):
        
        self.__computedLock[key].acquire()
        self.__computedDF[key] = self.__computedDF[key].append(additionalData,ignore_index = True)
        self.__mediator.send(key, additionalData.shape[0])
        self.__computedLock[key].release()

