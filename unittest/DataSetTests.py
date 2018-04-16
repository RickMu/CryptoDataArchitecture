import sys
sys.path.append("B:\\MyGit\\CryptoCoin\\solution")
from Repository.DataSet import DataSet
from DataProcessor.DataProcessor import DataProcessor
from Mediator.Mediator import ComputedAndDataMediator
import pandas as pd
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class DataSetUnitTests(TestCase):

    def setUp(self):
        self.dataProcessor = DataProcessor()
        self.filepath = 'B:\\MyGit\\CryptoCoin\\asset\\3daysCoinBase.csv'
        self.df = pd.read_csv(self.filepath)
        self.mediator = ComputedAndDataMediator()
        self.sut = DataSet(self.dataProcessor, self.mediator)

        def func(arg):
            return self.df
        self.dataProcessor.process = func
        self.sut.updateOriginal(self.df)
    
  
    def test_DataSet_Integrity(self):
        
        self.assertEqual(self.sut.getSize(), self.df.size)

        for x,y in zip(self.sut.getOriginalKeys(), self.df.keys()):
            self.assertEqual(x,y)

    def test_dataSet_Read(self):
        data = self.sut.read('price')
        self.assertEqual(data.size,self.df.price.size)

    def test_dataset_registerComputedColumn_Method(self):
        test = 'TEST1'        
       
        self.sut.registerComputedColumn(test)

        mock.assert_called_once()
        self.assertEqual(True, test in self.sut.getComputedKeys())

if __name__ == "__main__":
    unittest.main()
    


