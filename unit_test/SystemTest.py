import sys
sys.path.append("B:\\MyGit\\CryptoCoin\\solution")
from Repository.DataSet import DataSet
from DataProcessor.DataProcessor import DataProcessor
from Mediator.Mediator import ComputedAndDataMediator
import pandas as pd
import unittest
from unittest.mock import MagicMock
from unittest import TestCase
from ColumnRules.ColumnRule import ColumnRule
from Operators.Operator import OperatorType
from DataObject.ComputedColumns import OriginalColumn, ComputedColumn
from DataObject.DataObject import DataObject
from DataObject.ComputedDataObject import ComputedDataObject


class SystemTest (TestCase):
    def setUp(self):
        self.filepath = 'B:\\MyGit\\CryptoCoin\\asset\\3daysCoinBase.csv'
        self.df = pd.read_csv(self.filepath)
        self.df.set_index('time')

    def test_system_on_ComputeDataObject(self):
        mediator = ComputedAndDataMediator()
        dataProcessor = DataProcessor()
        ds = DataSet(dataProcessor, mediator)

        rule1 = ColumnRule([OriginalColumn.PRICE_MEAN,OriginalColumn.PRICE_MAX,OriginalColumn.PRICE_MIN],OperatorType.STOK,20)
        rule2 = ColumnRule([OriginalColumn.PRICE_MEAN],OperatorType.DIFF,1)
        identifier = str(ComputedColumn.MOMENTUM)+str(1)
        rule3 = ColumnRule([identifier],OperatorType.SUM,20)

        sut = ComputedDataObject((ComputedColumn.PRICE_STOK,20),ds,rule1,mediator)
        sut2 = ComputedDataObject((ComputedColumn.MOMENTUM,1),ds,rule2,mediator)
        sut3 = ComputedDataObject((ComputedColumn.MOMENTUM_SUM,20),ds,rule3,mediator)
        #print(sut.getRequiredColumns())

        ds.updateColumns(self.df)
        
        ds.updateColumns(self.df)

        cpCol = ds.read(sut.getName())
        col = sut.getData()
        print(len(cpCol))  
        self.assertEqual(cpCol.size,col.size)        
        self.assertNotEqual(cpCol.size, 0)

        cpCol = ds.read(sut2.getName())
        col = sut2.getData()
        print(len(cpCol))  
        
        self.assertEqual(cpCol.size,col.size)
        self.assertNotEqual(cpCol.size, 0)

        cpCol = ds.read(sut3.getName())
        col = sut3.getData()

        print(len(cpCol))         
        self.assertEqual(cpCol.size,col.size)
        self.assertNotEqual(cpCol.size, 0)


        

        #mock = MagicMock(name= 'onDataChange', return_value =1)
        #sut.onDataChange =mock


        #mock.assert_called_once()

if __name__ == "__main__":
    unittest.main()

