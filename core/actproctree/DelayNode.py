import queue

__author__ = 'cirreth'

import logging
from time import sleep
from core.actproctree.AbstractNode import AbstractNode


class DelayNode(AbstractNode):

    _required_fields = ['delay']

    def __init__(self, structure):
        super().__init__(structure)
        #node fields initialization
        self.delay = structure['delay']
        float(self.delay) #raise exception if delay is not number

    def action(self, parameters):
        sleep(self.delay)