from abc import abstractmethod

class ITransformer:

    @abstractmethod
    def mapInputToRequiredOutput(self,data):
        return


