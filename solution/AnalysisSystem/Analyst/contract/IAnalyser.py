from typing import List, Dict
import pandas as pd

from solution.AnalysisSystem.Decision.BaseDecision import BaseDecision
from solution.AnalysisSystem.Indicators.contracts.BaseIndicatorLite import BaseIndicatorLite


class IAnalyser:

    def analyse(self, newData : Dict[str,pd.Series], decision :BaseDecision):
        pass

    def getRequiredIndicators(self) -> List[BaseIndicatorLite]:
        pass