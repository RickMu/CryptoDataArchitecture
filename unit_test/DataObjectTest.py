import sys
sys.path.append("B:\\MyGit\\CryptoCoin\\solution")
from Repository.DataSet import DataSet
from DataProcessor.DataProcessor import DataProcessor
from Mediator.Mediator import ComputedAndDataMediator
import pandas as pd
import unittest
from unittest import TestCase
from ColumnRules.ColumnRule import ColumnRule
from Operators.Operator import OperatorType
from DataObject.ComputedColumns import OriginalColumn, ComputedColumn
from DataObject.DataObject import DataObject
from DataObject.ComputedDataObject import ComputedDataObject
from unittest.mock import MagicMock

class DataObjectTests(unittest.TestCase):

    def setUp(self):
        self.filepath = 'B:\\MyGit\\CryptoCoin\\asset\\3daysCoinBase.csv'
        self.df = pd.read_csv(self.filepath)
        self.df.set_index('time')
        self.mediator = ComputedAndDataMediator()
        self.dataProcessor = DataProcessor()
        self.ds = DataSet(self.dataProcessor, self.mediator)
        self.ds.updateColumns(self.df)
        return
    
    def test_DataObject_GetNameMethods(self):
        sut = DataObject(OriginalColumn.PRICE_MEAN,self.ds, self.mediator)
        self.assertEqual(sut.getName(),str(OriginalColumn.PRICE_MEAN))
    
    def test_DataObject_getData_Method(self):
        sut = DataObject(OriginalColumn.PRICE_MEAN,self.ds, self.mediator)
        data = sut.getData()
        d1 = self.ds.readPartial(str(OriginalColumn.PRICE_MEAN))
        self.assertEqual(data.size,d1.size)
    
    def test_ComputedDataObject_GetName_Method(self):
        #This is fucked, the self.register method is aids
        rule = ColumnRule([OriginalColumn.PRICE_MEAN,OriginalColumn.PRICE_MAX,OriginalColumn.PRICE_MIN],OperatorType.STOK,20)
        mock = MagicMock(name = "getRequiredColumns", return_value=1)
        rule.getRequiredIndicators = mock
        sut = ComputedDataObject((ComputedColumn.RSI,12),self.ds,rule, self.mediator)
     

        print(sut.getName())
        self.assertEqual(sut.getName(),  str(ComputedColumn.RSI)+str(12))
    
    

if __name__ == "__main__":
    unittest.main()