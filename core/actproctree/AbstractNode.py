import logging

__author__ = 'cirreth'

import re
import json
from queue import Queue
import datetime
from threading import Thread
from abc import abstractmethod, ABCMeta


class AbstractNode(metaclass=ABCMeta):

    _required_fields = []
    _general_required_fields = ['id', 'position']

    def __init__(self, structure):
        logging.debug(self.__class__.__name__+' constructor called: '+str(structure))
        self.__check_required_fields(structure)
        #general initialization
        self.id = structure['id']
        if 'next' in structure:
            self.next = structure['next']
        if 'exceptional' in structure:
            self.exceptional = structure['exceptional']


    @abstractmethod
    def action(self, parameters):
        pass

    def execute(self, parameters, async=True):
        if async:
            return self.execute_async(parameters).get()[0]
        else:
            return self.action(parameters)

    def execute_async(self, parameters):

        def wrapper(parameters, q):
            res = self.execute(parameters, async=False)
            q.put((res,))

        q = Queue()
        Thread(target=wrapper, args=(parameters, q)).start()
        return q

    def __check_required_fields(self, structure):
        for k in self._required_fields+self._general_required_fields:
            if k not in structure:
                raise Exception('Required field <'+k+'> not found in node: '+str(structure))
