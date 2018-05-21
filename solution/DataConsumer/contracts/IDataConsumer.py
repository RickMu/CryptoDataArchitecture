from abc import abstractmethod


class IDataConsumer:
    @abstractmethod
    def consume(self, data):
        return
