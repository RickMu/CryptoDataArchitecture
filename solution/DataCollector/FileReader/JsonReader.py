import time
import json
from solution.DataCollector.BaseDataProvider import BaseDataProvider
from solution.DataCollector.Schedular.Ec2ServerClient.Ec2DataTransformer import Ec2DataTransformer
from solution.DataConsumer.DataSetConsumer.OfflineDataConsumer import OfflineDataConsumer


class JsonReader(BaseDataProvider):

    def __init__(self, sourcePath, consumer :OfflineDataConsumer):
        super().__init__()
        self._sourcePath = sourcePath
        self._consumer = consumer

    def run(self) -> None:
        batch = 100000
        dataTransformer = Ec2DataTransformer()

        with open(self._sourcePath) as f:
            while True:
                if self._consumer.isReadyToConsume():
                        jsonData = []
                        for i in range(batch):
                            data = json.loads(f.readline())
                            jsonData.append(data)
                        data = dataTransformer.mapInputToRequiredOutput(jsonData)
                        self._consumer.consume(data)
                time.sleep(2)