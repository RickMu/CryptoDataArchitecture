from solution.AnalysisSystem.Indicators.contracts.IndicatorLite import IndicatorLite


class BaseIndicatorLite(IndicatorLite):

    def __init__(self, idTuple: tuple, ):
        self._idTuple = idTuple

    def toIdentifier(self) -> str:

        if len(self._idTuple) < 2:
            raise Exception ("ID Tuple should be of length 2, Given %s" % (str(idTuple)))

        return str(self._idTuple[0]) + str(self._idTuple[1])