from typing import Dict

import pandas as pd

from solution.AnalysisSystem.Decision.BaseDecision import BaseDecision


class IDecisionMaker:

    def decide(self, newData: Dict[str,pd.Series]) -> None:
        pass

    def getDecisions(self) -> BaseDecision:
        pass