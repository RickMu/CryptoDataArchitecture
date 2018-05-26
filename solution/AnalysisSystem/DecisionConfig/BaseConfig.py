from typing import List


class BaseConfig:

    def __init__(self,weighting: List[float], overlapCount: int):
        self._weighting = weighting
        self._overlapCount = overlapCount

    def getWeigthing(self) -> List[float]:
        return self._weighting

    def getOverlapCount(self) -> int:
        return self._overlapCount