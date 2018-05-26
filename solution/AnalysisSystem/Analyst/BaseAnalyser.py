from typing import List, Dict

from solution.AnalysisSystem.Analyst.contract.IAnalyser import IAnalyser
from solution.AnalysisSystem.Decision.BaseDecision import BaseDecision
from solution.AnalysisSystem.Indicators.contracts.BaseIndicatorLite import BaseIndicatorLite
from solution.DataObject.ComputedColumns import OriginalColumn
import pandas as pd


class BaseAnalyser(IAnalyser):

    def __init__(self):
        self._requriedCols: List[BaseIndicatorLite] = []

    def analyse(self, newData: Dict[str, pd.Series], decision: BaseDecision):

        buySellTuple, sellBuyTuple = self.__getTimeTupleBuySell(decision)
        requiredData = self.__getRequiredData(newData)

        return self._makeReport(requiredData, buySellTuple, sellBuyTuple)

    def _makeReport(self, data: Dict[str, pd.Series], buySellTuple: List[tuple], sellBuyTuple: List[tuple]):
        pass

    def __getRequiredData(self, newData: Dict[str, pd.Series]) -> Dict[str, pd.Series]:
        requiredData = {}
        for col in self._requriedCols:
            requiredData[col.toIdentifier()] = newData[col.toIdentifier()]

        return requiredData

    def __getTimeTupleBuySell(self, decision: BaseDecision) -> (List[tuple], List[tuple]):
        timeTuple = []
        for index, value in decision.getDecision().iteritems():
            timeTuple.append((index, value))

        buySellTimeTuple = []
        sellBuyTimeTuple = []
        for i in range(1, len(timeTuple)):
            if timeTuple[i - 1][1] == "buy" and timeTuple[i][1] == "sell":
                buySellTimeTuple.append((timeTuple[i - 1][0], timeTuple[i][0]))

            elif timeTuple[i - 1][1] == "sell" and timeTuple[i][1] == "buy":
                sellBuyTimeTuple.append((timeTuple[i - 1][0], timeTuple[i][0]))
            else:
                raise Exception("Wrong order, shouldn't have buy buy or sell sell: " + str(decision.getIdentifier()))

        return buySellTimeTuple, sellBuyTimeTuple

    def getRequiredIndicators(self) -> List[BaseIndicatorLite]:
        pass
