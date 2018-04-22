from abc import abstractmethod

class Consumer:

    def __init__(self):
        self._isReadyToConsume = False
    def isReadyToConsume(self):
        return self._isReadyToConsume
    def _toggleState(self):
        if self._isReadyToConsume is False:
            self._isReadyToConsume = True
        else:
            self._isReadyToConsume = False

    @abstractmethod
    def consume(self,data):
        return