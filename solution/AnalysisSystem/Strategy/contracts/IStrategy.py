import pandas as pd

class IStrategy:

    #Good To Buy
    def getInterestPoint(self, data :pd.Series) -> pd.Series:
        pass

    def _isInterestPoint(self, value) -> bool:
        pass