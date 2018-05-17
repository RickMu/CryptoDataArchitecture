from abc import abstractmethod

class ICollector:

    def __init__(self):
        self._consumers= []

    def addConsumer(self, consumer):
        self._consumers.append(consumer)

    def pushData(self,data):
        for i in self._consumers:
            i.push(data)

class IConsumer:
    @abstractmethod
    def push(self,data):
        return

