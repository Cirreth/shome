import logging
from plugins.SHomePlugin import SHomePlugin

__author__ = 'Кирилл'

class ProcExecPlugin(SHomePlugin):

    _action_processor = None

    def __init__(self, parameters):
        raise NotImplementedError('It is necessary to move this functionality to core')

    def call(self, reference, values={}):
        logging.debug('Process executor plugin'+reference)
        return self._action_processor.process(reference)

    def list(self, reference=''):
        return str(self._action_processor.pss_variables.keys())
