__author__ = 'cirreth'

from core.actproctree.AbstractNode import AbstractNode
from time import sleep
import logging

class DelayNode(AbstractNode):
    """Delay node. Nothing more"""

    """Delay interval"""
    _delay = None

    def __init__(self, process_tag, structure):
        super().__init__(process_tag, structure)
        logging.debug('Delay node constructing...')

    def __build__(self):
        self._delay = float(self._structure['delay'])
        self._next = self.create_direction('next')
        self._parallel = self.create_direction('parallel')
        self._exceptional = self.create_direction('exceptional')

    def execute(self, values={}):
        logging.debug('Executed DelayNode of'+self._process_tag+' with delay on '+str(self._delay))
        #CALL PARALLEL
        self.execute_direction(self._parallel, values)
        logging.debug('All parallel nodes of process '+self._process_tag+' completed')
        sleep(self._delay)
        #CALL NEXT
        self.execute_direction(self._next, values)
        logging.debug('All ways DelayNode completed')

    def get_node_required_keys(self):
        return ['interval']
