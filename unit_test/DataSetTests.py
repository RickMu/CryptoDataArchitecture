import sys
sys.path.append("B:\\MyGit\\CryptoCoin\\solution")
from solution.Repository.OriginalDataSet.DataSet import DataSet
from solution.DataProcessor.DataProcessor import DataProcessor
from solution.Mediator.Mediator import ComputedAndDataMediator
import pandas as pd
import unittest
from unittest import TestCase
from unittest.mock import MagicMock


class DataSetUnitTests(TestCase):

    def setUp(self):
        self.dataProcessor = DataProcessor()
        self.filepath = '..\\asset\\3daysCoinBase.csv'
        self.df = pd.read_csv(self.filepath)
        self.mediator = ComputedAndDataMediator()
        self.sut = DataSet(self.dataProcessor, self.mediator)

    def test_DataSet_Integrity(self):
        mock_mediator_send= MagicMock(name='send', return_value = None)
        self.mediator.send = mock_mediator_send
        mock_processor_process = MagicMock(name = 'process', return_value = self.df)
        self.dataProcessor.process = mock_processor_process

        self.sut.consume(self.df)

        self.assertEqual(self.sut.getSize(), self.df.shape[0])
        for x,y in zip(self.sut.getColumnNames(), self.df.keys()):
            self.assertEqual(x,y)

        mock_mediator_send.assert_called_once()
        mock_processor_process.assert_called_once()

    def test_dataSet_Read(self):

        mock_processor_process = MagicMock(name='process', return_value=self.df)
        self.dataProcessor.process = mock_processor_process

        self.sut.consume(self.df)
        data = self.sut.read('price')

        self.assertEqual(data.size,self.df.price.size)
        mock_processor_process.assert_called_once()

    def test_dataset_registerComputedColumn_Method(self):
        test = 'TEST1'
        self.sut.registerComputedColumn(test)
        self.assertEqual(True, test in self.sut.getComputedKeys())

    def test_check_consume_state_isCorrect(self):

        self.assertEqual(self.sut.isReadyToConsume(), True)
        self.sut.consume(self.df)
        self.assertEqual(self.sut.isReadyToConsume(), True)




if __name__ == "__main__":
    unittest.main()
    


