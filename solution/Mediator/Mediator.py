from Mediator.IMediator import Mediator
from collections import defaultdict
import pandas as pd

class ComputedAndDataMediator(Mediator):
    
    def __init__(self):
        self.__dataset = None
        self.__map = defaultdict(list)
    def setDataSet(self,dataset):
        self.__dataset = dataset


    #Enforcing that every computed object has to listen for a column
    def registerComputedColumns(self, dataobject, listenedColumn, listener):    
        self.__dataset.registerComputedColumns(dataobject.getName())
        self.__map[listenedColumn].append(listener)
    
    def send(self, name, updatedLength):
        dataSize = self.__dataset.getSize()
        threads = []
        for o in self.__map[name]:
            rqCols = o.getRequiredColumns()
            p = o.getPeriods()
            #the start position to get all requiredData
            rqDataSize= dataSize- p - updatedLength
            
            rqData = pd.DataFrame()
            for c in rqCols:
                rqData[c] = self.__dataset.readTail(c,rqDataSize)
            
            
            #might wish to do an async
            p = Thread(o.onDataChange, args= (rqData, updatedLength))
            p.start()
            threads.append(p)
        for p in threads:
                p.join()
        return 
            
    def respond(self,name, additionalData):
        self.__dataset.updateComputedColumns(name, additionalData)
        return 

if __name__ == "__main__":
    from collections import defaultdict
    from threading import Thread
    
    import pandas as pds