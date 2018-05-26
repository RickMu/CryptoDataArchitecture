from typing import List, Dict
import pandas as pd

from solution.AnalysisSystem.Decision.BaseDecision import BaseDecision
from solution.AnalysisSystem.DecisionConfig.BaseConfig import BaseConfig
from solution.AnalysisSystem.DecisionMakers.contracts.IDecisionMaker import IDecisionMaker
from solution.AnalysisSystem.Indicators.contracts.IndicatorLite import IndicatorLite
from solution.AnalysisSystem.Strategy.contracts.IStrategy import IStrategy


class DecisionMaker(IDecisionMaker):

    def __init__(self, indicators : List[IndicatorLite], strategies : List[IStrategy], config: BaseConfig):
        self._indicators = indicators
        self._strategies = strategies
        self._config = config
        self._decision = None
        self._createDecision()

    def _createDecision(self):
        name = ''
        for i in self._indicators:
            name += (","+i.toIdentifier())
        self._decision = BaseDecision(name)

    def decide(self, newData: Dict[str ,pd.Series]) -> None:
        points = []
        for indicator,strategy in zip(self._indicators, self._strategies):
            interestPoints = strategy.getInterestPoint(newData[indicator.toIdentifier()])
            points.append(interestPoints)

        overlapSeries = abs(points[0])
        for i in range(1,len(points)):
            overlapSeries = overlapSeries + abs(points[i])
        overlapSeries.transform(self._transformFunc)

        for i in range(len(points)):
            points[i] = self._config.getWeigthing()[i] * points[i]

        totalPoint = points[0]
        for i in range(1,len(points)):
            totalPoint = totalPoint + points[i]

        totalPoint = totalPoint * overlapSeries
        self._decision.decide(totalPoint)

    def _transformFunc(self,value):
        if value == self._config.getOverlapCount():
            return 1
        else:
            return 0

    def getDecisions(self) -> BaseDecision:
        return self._decision


