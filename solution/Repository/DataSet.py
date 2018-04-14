import pandas as pd
from threading import Lock, Thread
from collections import defaultdict


class DataSet:
    
    def __init__(self, processor, mediator):
        self.__originalDF = pd.DataFrame()
        self.__uncompressedDF = pd.DataFrame()
        self.__computedDF = defaultdict(pd.Series)
        self.__computedLock = defaultdict(Lock)
        self.__datalock = Lock()
        self.__originalColumnListeners = []
        self.__computedColumnListeners = defaultdict(list)
        self.__dataProcessor = processor
        self.__mediator = mediator
        self.__mediator.setDataSet(self)
        
    def getSize(self):
        return self.__originalDF.size
    
    def getOriginalKeys(self):
        return self.__originalDF.keys()
    
    def getComputedKeys(self):
        return self.__computedDF.keys()
        
    def updateOriginal(self,additionalData):
        self.__datalock.acquire()    
        
        data = self.__dataProcessor.process(additionalData)
        
        self.__originalDF = self.__originalDF.append(data)
        
        self.__mediator.send('original', data)
        
        self.__datalock.release()
    #method should be retired
    def getAllData(self):
        return self.__originalDF
    def read(self,key):
        return self.readTail(key)
        # log it or print?
    
    def readTail(self,key, count = None):
        data= None
        if key in self.__originalDF.keys():
            data = self.__originalDF[key]
        if key in self.__computedDF.keys():
            data = self.__computedDF[key]
        if data is None:
            raise Exception("No specified key in \n%s \n%s" % (self.__originalDF.keys(), self.__computedDF.keys()))

        if count is not None:
            data = data[count:]

            
        return data
        
    def registerComputedColumn(self, computedColumnName):
        self.__computedDF[computedColumnName] = pd.Series()
        self.__computedLock[computedColumnName] = Lock()
    
    def updateComputedColumns(self,key,additionalData):
        
        self.__computedLock[key].acquire()
        
        self.__computedDF[key].append(additionalData,ignore_index = True)
        
        self.__mediator.send(key, additionalData)
        
        self.__computedLock[key].release()
    