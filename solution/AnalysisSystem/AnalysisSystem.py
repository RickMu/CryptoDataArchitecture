from typing import List

from solution.AnalysisSystem.Analyst.RevenueAnalyser import RevenueAnalyser
from solution.AnalysisSystem.Analyst.contract.IAnalyser import IAnalyser
from solution.AnalysisSystem.DecisionConfig.BaseConfig import BaseConfig
from solution.AnalysisSystem.DecisionMakers.DecisionMaker import DecisionMaker
from solution.AnalysisSystem.DecisionMakers.contracts.IDecisionMaker import IDecisionMaker
from solution.AnalysisSystem.Indicators.contracts.BaseIndicatorLite import BaseIndicatorLite
from solution.AnalysisSystem.Strategy.contracts.IStrategy import IStrategy
from typing import Dict
import pandas as pd

from solution.DataProcessor.DataSourceClient.contracts.IClient import IClient
from solution.DataSetListener.AnalysisSystemDataListener import AnalysisSystemDataListener


class AnalysisSystem:

    def __init__(self, ):
        self._decisionMakers :List[IDecisionMaker] = []
        self._otherRequiredCols = []
        self._indicators : List[BaseIndicatorLite] = []
        self._analyserIndicator: List[BaseIndicatorLite] = []
        self._datalistener = None
        self._analysers :List[IAnalyser] = []
        self._defaultAnalyser()
        pass

    def setToEvaluate(self, identifier: tuple, strategy :IStrategy, configTuple:tuple):

        indicator = BaseIndicatorLite(identifier)
        self._indicators.append(indicator)
        self._decisionMakers.append(DecisionMaker([indicator],[strategy], BaseConfig(configTuple[0], configTuple[1])))

    #Not exactly a callback, a call back should run on another thread than the thread calling this.
    def onDataUpdateCallBack(self, data:Dict[str,pd.Series], analyserData : [str,pd.Series]):

        for a in self._analysers:
            for decider in self._decisionMakers:
                decider.decide(data)
                revList, missedRevList, revSum, missedReveSum = a.analyse(analyserData, decider.getDecisions())
                print("Analyser: " + str(revList) )
                print("Rev Sum: " + str(revSum) + "Missed Rev Sum: " + str(missedReveSum))

    def _defaultAnalyser(self):
        self._analysers .append(RevenueAnalyser())

        for a in self._analysers:
            for indicator in a.getRequiredIndicators():
                self._analyserIndicator.append(indicator)

    def getAnalysisSystemDatalistener(self, client:IClient):
        if self._datalistener is None:
            self._datalistener = AnalysisSystemDataListener(client,self.onDataUpdateCallBack,self._indicators,self._analyserIndicator)
        return self._datalistener


