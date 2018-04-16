import sys
sys.path.append("B:\\MyGit\\CryptoCoin\\solution")
from Repository.DataSet import DataSet
from DataProcessor.DataProcessor import DataProcessor
from Mediator.Mediator import ComputedAndDataMediator
import pandas as pd
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from ColumnRules.ColumnRule import ColumnRule
from Operators.Operator import OperatorType
from DataObject.ComputedColumns import OriginalColumn, ComputedColumn
from DataObject.DataObject import DataObject
from DataObject.ComputedDataObject import ComputedDataObject

class MediatorTest (TestCase):

    def setUp(self):
        self.sut = ComputedAndDataMediator()
        self.filepath = 'B:\\MyGit\\CryptoCoin\\asset\\3daysCoinBase.csv'
        self.df = pd.read_csv(self.filepath)
        self.df.set_index('time')
        self.dataProcessor = DataProcessor()
        self.ds = DataSet(self.dataProcessor, self.sut)
        
        
        self.sut.setDataSet(self.ds)
    
    def test_dataobject_register_method(self):
        mock = MagicMock(name='foo',return_value='ok')
        self.ds.registerComputedColumn

        o1 = ComputedDataObject((ComputedColumn.RSI,12),None,None, self.sut)
        o2 =ComputedDataObject((ComputedColumn.RSI,12),None,None, self.sut)

        self.sut.registerComputedColumn(o1,'Original',o1)
        self.sut.registerComputedColumn(o2,'Original',o2)
        

        self.assertEqual(True, o1 in self.sut.getMap()['Original'])
        
        self.assertEqual(True, o2 in self.sut.getMap()['Original'])

        
if __name__ == "__main__":
    unittest.main()