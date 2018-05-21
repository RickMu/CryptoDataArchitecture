import time

from solution.DataCollector.BaseDataProvider import BaseDataProvider

import pandas as pd

from solution.DataConsumer.DataSetConsumer.OfflineDataConsumer import OfflineDataConsumer


class CsvReader(BaseDataProvider):

    def __init__(self, sourcePath, consumer :OfflineDataConsumer):
        super().__init__()
        self._sourcePath = sourcePath
        self._consumer = consumer

    def run(self) -> None:
        datasource = pd.read_csv(self._sourcePath, squeeze=True)
        if datasource.empty:
            raise Exception("File Read is Empty")
        datasource.sort_index(inplace=True)
        batch = 10000

        while True:
            if self._consumer.isReadyToConsume():
                self._consumer.consume(datasource[:batch])
                datasource = datasource[batch:]
            time.sleep(5)





