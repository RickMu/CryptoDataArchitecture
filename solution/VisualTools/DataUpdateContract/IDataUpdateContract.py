from abc import abstractmethod


class DataUpdateListener:
    @abstractmethod
    def onDataUpdate(self, data):
        return


class DataUpdateSubject:
    @abstractmethod
    def addListener(self, listener):
        return

    @abstractmethod
    def notify(self, data):
        return
