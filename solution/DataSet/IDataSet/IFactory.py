from abc import abstractmethod

'''
Factories are meant to be responsible for the creation of indicators, signals, etc based on configs
'''
class IFactory:

    @abstractmethod
    def create(self,configs):
        return