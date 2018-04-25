from solution.DataSet.DataAccessor.IDataAccessor import IDataAccessor
class DataSetAccessor(IDataAccessor):

    def __init__(self,dataset):
        IDataAccessor.__init__(self,dataset)

    def read(self, key, length, TailUp=True):
        self.__checkColumnExists(key)
        allData = self._dataset.getColumn(key)

        if TailUp:
            startPos = allData.shape[0] - length
            if startPos <0:
                startPos= 0
            allData = allData[startPos:]
        return allData

    def __checkColumnExists(self, name):
        allNames = self._dataset.getColumnNames()

        if name not in allNames:
            raise Exception("Given Column Name %s is not in data set %s" % (name, allNames))


