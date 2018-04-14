from DataObject.DataObject import DataObject
class ComputedDataObject(DataObject):
    
    def __init__(self,identifier,dataset,rule,mediator):
        super().__init__(identifier,dataset)
        self.__rule = rule
        self.__mediator = mediator
    
    def setPeriod(self,periods):
        self.__periods= periods
    #override
    def onDataChange(self,requiredData,updatedLength):
        additionalData = self.compute(requiredData,updatedLength)
        
        if requiredData.size > updatedLength:
            additionalData= additionalData[self.__periods]
            
        self.__mediator.respond(additionalData,self.getName())
        
    
    def getPeriods(self):
        return self.__periods
    
    def getRequiredColumns(self):
        return self.__rule.getRequiredColumns()
    
    def compute(self,requiredData,updatedLength):
        computedData = self.__rule.compute(requiredData, self.__periods, 'PriceMean',updatedLength)
        return computedData