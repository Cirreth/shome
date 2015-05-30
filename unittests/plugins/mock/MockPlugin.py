__author__ = 'cirreth'
from plugins.SHomePlugin import SHomePlugin
import logging

class MockPlugin(SHomePlugin):

    def __init__(self, parameters):
        logging.debug('MockPlugin initialization')

    def call(self, reference, values={}):
        return self._execute(reference)

    def _execute(self, command):
        print('execute mock! '+command)
        return command

    def list(self, reference=''):
        return 'Any value'