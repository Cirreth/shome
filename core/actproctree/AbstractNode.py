__author__ = 'cirreth'

from abc import abstractmethod, ABCMeta
import datetime
import re
from threading import Thread
import logging
import json

class AbstractNode(metaclass=ABCMeta):

    """Absctract node class attribute"""
    _action_processor = None
    _required_keys = ['type']
    """node json structure"""
    _structure = None
    _process_tag = None
    _performer = None
    _scheduler = None

    """To be executed after current node"""
    _next = None

    """Works in the same time that the current node"""
    _parallel = None

    """Exceptional directions to be executed if execute method catch exception"""
    #@TODO Not implemented
    _exceptional = None

    """Node variables"""
    _variables = {}

    @abstractmethod
    def __init__(self, process_tag, structure):
        logging.debug('AbstractNode constructor call ( '+json.dumps(structure)+' )')
        self._process_tag = process_tag
        self._required_keys.append(self.get_node_required_keys())
        if self.__class__.__name__ != structure['type'][1:-1]:
            raise Exception(self.__class__.__name__+' expected but '+structure['type'][1:-1]+' found')
        #@TODO DEBUG CODE BELOW
        #if not all([k for k in self._required_keys]):
        #    raise MissedParameterException(self.__class__.__name__+' expected but '+structure['type'][1:-1]+' found')
        self._structure = structure
        self._performer = AbstractNode._performer
        self._scheduler = AbstractNode._scheduler
        self.__build__()

    @abstractmethod
    def __build__(self):
        """build the node based on structure attribute"""

    @abstractmethod
    def get_node_required_keys(self):
        """required node parameters list"""

    @abstractmethod
    def execute(self, values={}):
        """perform node action"""

    #@TODO ActionProcessor duplicate!
    def parse_level(ci):
        if re.search('^\\s*\\[', ci): #array of objects
            return [{k: json.dumps(v) for k, v in e.items()} for e in json.loads(ci)]
        else:
            return {k: json.dumps(v) for k, v in json.loads(ci).items()}

    def create_direction(self, name):
        if name in self._structure:
            field = self._action_processor.create_node_direction(self._process_tag, self._structure[name])
            return field
        else:
            return None

    def execute_direction(self, direction, values):
        """
            Execute from nodes from direction.
        """
        if direction:
            threads = []
            for d in direction:
                if isinstance(d, str):
                    threads.append(Thread(target=self._action_processor.process, args=d))
                else:
                    threads.append(Thread(target=d.execute, args=(values, )))
            for t in threads:
                logging.debug('Thread started')
                t.start()
            for t in threads:
                logging.debug('node from process '+self._process_tag+' thread joined to main')
                t.join()

    def prepare_ref(self, reference, values):
        """Replace tokens in reference to values"""
        pvars = self._action_processor.pss_variables
        ref = ''
        lst = 0
        tknval = None
        for c in re.finditer('<@?[a-zA-Z0-9_-]+?>', reference):
            name = c.group(0)[1:-1] #variable name
            logging.debug('AbstractNode_PF: var with name ( '+name+' ) found')
            #looking for value
            #if keyword
            kw = self.replace_keyword(name)
            if kw:
                logging.debug('... and detected as keyword')
                tknval = kw
            #in user sended values
            elif name in values:
                logging.debug('... and detected as value')
                tknval = values[name]
            #in global process storage and variable defined
            elif self._process_tag in pvars and name in pvars[self._process_tag]:
                logging.debug('... and name in process variables')
                tknval = pvars[self._process_tag][name]
                if isinstance(tknval, dict):
                    #if dictionary with single value
                    if len(tknval) == 1: tknval = next(iter(tknval.values()))
            elif name in self._variables:
                logging.debug('... and name in variables')
                tknval = self._variables[name]
            if tknval: ref += reference[lst:c.start(0)]+str(tknval)
            lst = c.end(0)
        ref += self._reference[lst:]
        return ref

    @staticmethod
    def replace_keyword(keyword):
        if keyword == '@DATETIME':
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif keyword == '@TIME':
            return datetime.datetime.now().strftime('%H:%M:%S')
        elif keyword == '@TIME_HM':
            return datetime.datetime.now().strftime('%H:%M')
        elif keyword == '@DATE':
            return datetime.datetime.now().strftime('%Y-%m-%d')
        else:
            return False