
import pandas as pd

class BaseDecision:

    def __init__(self, identifier: str):
        self._decisions = pd.Series()
        self._lastDecision = "sell"
        self._identifier = identifier
        self._recentDecision = None

    def getIdentifier(self):
        return self._identifier

    def decide(self,dataToBinarise: pd.Series):
        indexes = []
        values = []
        for index, value in dataToBinarise.iteritems():

            if value>0 and self._lastDecision == "sell":
                self._lastDecision = "buy"
                indexes.append(index)
                values.append("buy")

            if value < 0 and self._lastDecision == "buy":
                self._lastDecision = "sell"
                indexes.append(index)
                values.append("sell")
        self._recentDecision = pd.Series(values, index=indexes)
        self._decisions = self._decisions.append(self._recentDecision)

    def getDecision(self):
        return self._decisions

    def getRecentDecision(self):
        return self._recentDecision
