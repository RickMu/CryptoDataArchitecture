import pandas as pd
from threading import Lock, Thread
from collections import defaultdict
from solution.DataCollector.Worker.WorkableState import Consumer
from solution.Repository.IDataSet.IDataSet import IDataSet

class DataSet(Consumer,IDataSet):
    SINGLE_KEY = "ORIGINAL"
    def __init__(self, processor):
        Consumer.__init__(self)
        self.__originalDF = pd.DataFrame(dtype=float)
        self.__datalock = Lock()
        self.__listener = None
        self.__dataProcessor = processor
        super()._toggleState()
        
    def getSize(self):
        return self.__originalDF.shape[0]

    def consume(self,data):
        self.updateColumns(data)

    #For this dataset, all the data columns are going to come at once
    #So for now updating single columns won't be implemented
    def updateColumn(self,key,data):
        raise Exception("Unimplemented Method")

    def updateColumns(self, data):
        self.__datalock.acquire()
        super()._toggleState()

        data = self.__dataProcessor.process(data)
        self.__originalDF = self.__originalDF.append(data)
        self.notify(data.shape[0])

        print("******************This is in dataset**********************")
        print(self.__originalDF.shape[0])

        super()._toggleState()
        self.__datalock.release()

    #making it so that every dataset only has one listener
    def addUpdateListener(self,listener):
        self.__listener = listener

    def notify(self,updatedlength):
        if self.__listener is None:
            return
        self.__listener.notify(updatedlength)

    def getColumn(self, name):
        return self.__originalDF[name]

    def getColumnNames(self):
        return self.__originalDF.keys()
