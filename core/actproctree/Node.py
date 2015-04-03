from sqlalchemy import orm

__author__ = 'cirreth'

import logging
from queue import Queue
from threading import Thread
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

"""

"""

    def __exec_wrapper(self, parameters, q):
        res = self.execute(parameters, async=False)
        q.put((res,))
        return q

    def execute(self, parameters, async=True):
        q = Queue()
        if async:
            Thread(target=self.__exec_wrapper, args=(parameters, q)).start()
        else:
            res = self.action(parameters)
            q.put((res,))
        return q

    def __check_required_fields(self, structure):
        for k in self._required_fields+self._general_required_fields:
            if k not in structure:
                raise Exception('Required field <'+k+'> not found in node: '+str(structure))

    @classmethod
    def create(cls, structure):
        #imports
        #@TODO How can i implement factory method w/o circular import?
        from core.actproctree.DelayNode import DelayNode
        from core.actproctree.RequestNode import RequestNode
        #structure = json.loads(expression)
        node_type = structure['type']
        if node_type == 'RequestNode':
            return RequestNode(structure)
        elif node_type == 'DelayNode':
            return DelayNode(structure)