from solution.DataSet.DataAccessor.IDataAccessor import IDataAccessor
class DataSetAccessor(IDataAccessor):

    def __init__(self,dataset, parent = None):
        IDataAccessor.__init__(self,dataset,parent)

    def read(self, key, length, TailUp=True):
        if self.__checkColumnExists(str(key)) is False:
            allData = self.parent.read(key,length)
        else:
            allData = self._dataset.getColumn(str(key))

            if TailUp:
                startPos = allData.shape[0] - length
                if startPos <0:
                    startPos= 0
                allData = allData[startPos:]
        return allData

    def getColumnNames(self):
        return self._dataset.getColumnNames()

    def __checkColumnExists(self, name):
        allNames = self._dataset.getColumnNames()



        if name not in allNames:
            if self.parent is None:
                raise Exception("Exception No Required Column %s " % (name))
            return False

        return True


