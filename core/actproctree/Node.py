__author__ = 'cirreth'

import logging
from queue import Queue
from abc import abstractmethod, ABCMeta


class Node(metaclass=ABCMeta):

    _directions = ['next', 'parallel', 'exceptional']

    _general_required_fields = ['id', 'position']

    def __init__(self, structure):
        logging.debug(self.__class__.__name__+' constructor called: '+str(structure))
        self.__check_required_fields(structure)
        #general initialization
        self.id = structure['id']
        #fields initialization
        for p in self._required_fields+self._optional_fields:
            if p in structure:
                self.__setattr__(p, structure[p])

    @abstractmethod
    def action(self, parameters):
        pass

    def execute(self, parameters):
        q = Queue()
        res = self.action(parameters)
        q.put((res, self._directions['next']))
        return q, self._directions['parallel']

    def __check_required_fields(self, structure):
        for k in self._required_fields+self._general_required_fields:
            if k not in structure:
                raise Exception('Required field "'+k+'" not found in node: '+str(structure))