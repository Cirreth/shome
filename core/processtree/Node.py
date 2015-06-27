import re
from threading import Thread
import datetime

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
        #directions initialization
        for d in self._directions:
            self.__setattr__(d, structure[d] if d in structure else [])

    @abstractmethod
    def action(self, parameters):
        pass

    def async_wrapper(self, q, parameters):
        res = self.action(parameters)
        direction_next = self.next if 'next' in self._directions else []
        q.put((res, direction_next))

    def node_exec(self, parameters, async=False):
        q = Queue()
        if async:
            Thread(target=self.async_wrapper, args=(q, parameters)).start()
        else:
            res = self.action(parameters)
            direction_next = self.next if 'next' in self._directions else []
            q.put((res, direction_next))
        return q, self.parallel if 'parallel' in self._directions else []

    def execute(self, parameters):
        return self.node_exec(parameters)

    @classmethod
    def substitute_placeholders(cls, text, parameters, skipped_as_null=False):
        """
        :param text: Text to be replaced
        :param parameters: List of keywords
        :param skipped_as_null: If it is True, skipped variables will be replaced to js keyword 'null'
        :return:
        """
        if text is None:
            return None
        res = ''
        last_idx = 0
        for m in re.finditer('\[@?[a-zA-Z0-9-_]*?\]', text):
            name = m.group(0)[1:-1]
            if name in parameters:
                val = str(parameters[name])
            else:
                val = Node.replace_keyword(name)
                if val is None and skipped_as_null:
                    val = 'null'
            res += text[last_idx:m.start(0)]+val
            last_idx = m.end(0)
        res += text[last_idx:]
        res = res.replace('True', 'true').replace('False', 'false')
        return res

    @staticmethod
    def replace_keyword(keyword):
        if keyword == '@DATE':
            return datetime.datetime.now().strftime('%d.%m.%Y')
        elif keyword == '@DATETIME':
            return datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        elif keyword == '@TIME':
            return datetime.datetime.now().strftime('%H:%M:%S')
        else:
            return 'null'

    def __check_required_fields(self, structure):
        for k in self._required_fields+self._general_required_fields:
            if k not in structure:
                raise Exception('Required field "'+k+'" not found in node: '+str(structure))