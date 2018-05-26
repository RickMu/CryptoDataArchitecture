from typing import List, Dict

import pandas as pd

from solution.AnalysisSystem.Analyst.BaseAnalyser import BaseAnalyser
from solution.AnalysisSystem.Indicators.contracts.BaseIndicatorLite import BaseIndicatorLite
from solution.DataObject.ComputedColumns import OriginalColumn


class RevenueAnalyser(BaseAnalyser):
    def __init__(self):
        super().__init__()

    def _makeReport(self, data: Dict[str, pd.Series], buySellTuple: List[tuple], sellBuyTuple: List[tuple]):

        pricemean = data[self._requriedCols[0].toIdentifier()]

        revenue = []
        sumRev = 0
        for buySell in buySellTuple:
            boughtPrice = pricemean.loc[buySell[0]]
            sellPrice = pricemean.loc[buySell[1]]
            revSum = (sellPrice - boughtPrice) / boughtPrice
            revenue.append(
                ( revSum, buySell[0], buySell[1])
            )
            sumRev += revSum

        revenueMissed = []
        missedRev = 0
        for buySell in sellBuyTuple:
            soldPrice = pricemean.loc[buySell[0]]
            buyPrice = pricemean.loc[buySell[1]]
            missedRevenue = (buyPrice - soldPrice) / soldPrice
            revenueMissed.append(
                (missedRevenue , buySell[0], buySell[1])
            )
            missedRev += missedRevenue

        return revenue, revenueMissed, sumRev, missedRev

    def getRequiredIndicators(self) -> List[BaseIndicatorLite]:
        if not self._requriedCols:
            col = BaseIndicatorLite((OriginalColumn.PRICE_MEAN, ""))
            self._requriedCols.append(col)
        return self._requriedCols
