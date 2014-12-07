__author__ = 'cirreth'
from abc import abstractmethod, ABCMeta

class SHomePlugin(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, parameters):
        pass

    @abstractmethod
    def call(self, reference, values={}):
        pass

    @abstractmethod
    def list(self, reference=''):
        pass