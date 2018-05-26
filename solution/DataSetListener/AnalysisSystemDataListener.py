from typing import List

from solution.AnalysisSystem.Indicators.contracts.IndicatorLite import IndicatorLite
from solution.DataProcessor.DataSourceClient.contracts.IClient import IClient
from solution.DataSetListener.contracts.IDataSetListener import BaseDataSetListener


class AnalysisSystemDataListener(BaseDataSetListener):

    def __init__(self, client: IClient, callbackFunc ,indicators :List[IndicatorLite], analyserIndicators: List[IndicatorLite]):
        super().__init__(client)
        self._requiredIndicators = indicators
        self._callbackFunc = callbackFunc
        self._analyserIndicators = analyserIndicators

    def onDataUpdate(self, event) -> None:
        data = {}
        analyserData = {}
        for indicator in self._requiredIndicators:
            key = indicator.toIdentifier()
            data[key] = self._client.readFromTail(key, event)
        for analyserIndicator in self._analyserIndicators:
            key = analyserIndicator.toIdentifier()
            analyserData[key] = self._client.read(key)

        self._callbackFunc(data, analyserData)