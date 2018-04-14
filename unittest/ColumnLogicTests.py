import sys
sys.path.append("B:\\MyGit\\CryptoCoin\\solution")
import unittest
from ColumnRules.ColumnRule import ColumnRule
from Repository.DataSet import DataSet
from Mediator.Mediator import ComputedAndDataMediator
from DataProcessor.DataProcessor import DataProcessor
from Operators.Operator import OperatorType
import pandas as pd
class LogicTests(unittest.TestCase):

    def setUp(self):
        self.filepath = 'B:\\MyGit\\CryptoCoin\\asset\\3daysCoinBase.csv'
        self.df = pd.read_csv(self.filepath)
        self.df.set_index('time')
        self.mediator = ComputedAndDataMediator()
        self.dataProcessor = DataProcessor()
        self.ds = DataSet(self.dataProcessor, self.mediator)
       
        self.sut = ColumnRule(['PriceMean'], OperatorType.DIFF)
        
    def test_processor(self):
        data = self.dataProcessor.process(self.df)
        self.assertNotEqual(data.size,0)
        self.assertNotEqual(self.dataProcessor.getCachedData().size,0)
        print('OK')

    def test_DifferenceTest(self):
        self.ds.updateOriginal(self.df)

        data = self.ds.read('PriceMean')
        df = pd.DataFrame()
        df['PriceMean'] = data

        diff = self.sut.compute(df,8,'Diff',data.size)

        self.assertEqual(data.size,diff.size)

if __name__ == "__main__":
    unittest.main()
    



