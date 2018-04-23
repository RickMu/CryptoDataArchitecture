
import unittest
from ColumnRules.ColumnRule import ColumnRule
from Repository.DataSet import DataSet
from Mediator.Mediator import ComputedAndDataMediator
from DataProcessor.DataProcessor import DataProcessor
from Operators.Operator import OperatorType
from DataObject.ComputedColumns import OriginalColumn, ComputedColumn

class LogicTests(unittest.TestCase):

    def setUp(self):
        self.filepath = 'B:\\MyGit\\CryptoCoin\\asset\\3daysCoinBase.csv'
        self.df = pd.read_csv(self.filepath)
        self.df.set_index('time')
        self.mediator = ComputedAndDataMediator()
        self.dataProcessor = DataProcessor()
        self.ds = DataSet(self.dataProcessor, self.mediator)
        self.ds.updateColumns(self.df)
        
    def test_processor(self):
        data = self.dataProcessor.process(self.df)
        self.assertNotEqual(data.size,0)
        self.assertNotEqual(self.dataProcessor.getCachedData().size,0)
        print('OK')

    def test_DifferenceTest(self):
        sut = ColumnRule([OriginalColumn.PRICE_MEAN], OperatorType.DIFF,1)
        data = self.ds.read(OriginalColumn.PRICE_MEAN)
        df = pd.DataFrame()
        df[(OriginalColumn.PRICE_MEAN)] = data
        diff = sut.compute(df,data.size,)
        self.assertEqual(data.size,diff.size)
    def test_STOK(self):
        d1 = self.ds.read(OriginalColumn.PRICE_MEAN)
        d2 = self.ds.read(OriginalColumn.PRICE_MIN)
        d3 = self.ds.read(OriginalColumn.PRICE_MAX)
        df = pd.DataFrame()
        df[OriginalColumn.PRICE_MEAN] = d1
        df[OriginalColumn.PRICE_MAX] = d2
        df[OriginalColumn.PRICE_MIN] = d3

        sut = ColumnRule([OriginalColumn.PRICE_MEAN,OriginalColumn.PRICE_MAX,OriginalColumn.PRICE_MIN],OperatorType.STOK,20)
        stok = sut.compute(df,d1.size-20)
        
        self.assertEqual(stok.size, d1.size-20)
    
    def test_getRequiredCols_Method(self):
        rqCols =[OriginalColumn.PRICE_MEAN,OriginalColumn.PRICE_MAX,OriginalColumn.PRICE_MIN]
        sut = ColumnRule(rqCols,OperatorType.STOK,20)

        for i,j in zip(sut.getRequiredColumns(),rqCols):
            self.assertEqual(i,j)

        MomentumAvgP1 = str(ComputedColumn.MOMENTUM_AVG)+str(1)

        sut = ColumnRule([MomentumAvgP1],OperatorType.STOK,20)
        self.assertEqual(sut.getRequiredColumns(),  [MomentumAvgP1]  )

if __name__ == "__main__":
    import pandas as pd
    #unittest.main()
    



