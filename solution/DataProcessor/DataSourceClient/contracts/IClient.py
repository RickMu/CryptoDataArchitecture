from abc import abstractmethod
import pandas as pd

class IClient:

    def insert(self,data) -> None:
        pass

    def readyToConsume(self) -> bool:
        pass

    def read(self,key) -> pd.Series:
        pass

    def readFromTail(self,key,length) -> pd.Series:
        pass

    # This should just be a temp solution
    def readAllData(self)-> dict:
        pass

    def addAdditionalSystem(self,additionalSystem) -> None:
        pass