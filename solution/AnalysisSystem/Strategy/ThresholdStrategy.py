import pandas as pd

from solution.AnalysisSystem.Strategy.contracts.IStrategy import IStrategy


class ThresholdStrategy(IStrategy):

    def __init__(self,buyThreshold, sellThreshold):
        self._buyThreshold = buyThreshold
        self._sellThreshold = sellThreshold

    def getInterestPoint(self, data: pd.Series) -> pd.Series:

        interestPoints = data.transform(self._transformFunc)
        return interestPoints

    def _transformFunc(self,x):
        if x <= self._buyThreshold:
            return 1
        elif x >= self._sellThreshold:
            return -1
        else:
            return 0

    def _isInterestPoint(self, value) -> bool:
        return super()._isInterestPoint(value)