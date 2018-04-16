from DataObject.DataObject import DataObject
from DataObject.ComputedColumns import OriginalColumn
class ComputedDataObject(DataObject):
    
    def __init__(self,identifier,dataset,rule,mediator):
        super().__init__(identifier,dataset,mediator)
        self.__rule = rule
        self.register()
       
    def register(self):
        cols = self.getRequiredColumns()
        originalCols = True
        for i in cols:
            if i not in OriginalColumn:
                originalCols = False
        if originalCols:
            cols = ['Original']
        
        if len(cols) > 1:
            raise Exception("Listening to two or more computed column is not yet supported")
        
        self._mediator.registerComputedColumn(self,cols[0],self)

    def getPeriods(self):
        return self.__rule.getPeriods()


    def getName(self):
        return str(self._identifier[0])+str(self._identifier[1])
    #override
    def onDataChange(self,requiredData,updatedLength):
        additionalData = self.compute(requiredData,updatedLength)
        
        self._mediator.respond(self.getName(),additionalData)

    def getRequiredColumns(self):
        return self.__rule.getRequiredColumns()

    def compute(self,requiredData,updatedLength):
        computedData = self.__rule.compute(requiredData, updatedLength)
        return computedData