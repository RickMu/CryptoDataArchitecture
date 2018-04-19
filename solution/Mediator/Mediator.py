from Mediator.IMediator import Mediator
from collections import defaultdict
import pandas as pd
from threading import Thread

class ComputedAndDataMediator(Mediator):
    
    def __init__(self):
        self.__dataset = None
        self.__map = defaultdict(list)

    def setDataSet(self,dataset):
        self.__dataset = dataset

    def getMap(self):
        return self.__map

    #Enforcing that every computed object has to listen for a column
    def registerComputedColumn(self, dataobject, listenedColumn, listener):    
        self.__dataset.registerComputedColumn(dataobject.getName())
        self.__map[listenedColumn].append(listener)
    
    def registerOriginalColumn(self,listener):
        self.__map['Original'].append(listener)

    def send(self, name, updatedLength):
        threads = []
        for o in self.__map[name]:
            rqCols = o.getRequiredColumns()
            p = o.getPeriods()
            #the start position to get all requiredData
            rqDataSize= p+ updatedLength

            #print(rqDataSize)
            rqData = pd.DataFrame()
            for c in rqCols:
                rqData[c] = self.__dataset.readTail(c,rqDataSize)

            #might wish to do an async
            p = Thread(target= o.onDataChange, args= (rqData, updatedLength))
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