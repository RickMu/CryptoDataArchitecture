from abc import abstractmethod

class ITransformer:

    @abstractmethod
    def mapInputToRequiredOutput(self,input):
        return


