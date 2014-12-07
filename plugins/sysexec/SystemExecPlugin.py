import logging
import subprocess
from plugins.SHomePlugin import SHomePlugin

__author__ = 'Кирилл'

class SystemExecPlugin(SHomePlugin):

    def __init__(self, parameters):
        logging.debug('SystemExecPlugin initialization')

    def call(self, reference, values={}):
        logging.debug('Reading from SystemExecPlugin')
        return self._execute(reference)

    def _execute(self, command):
        p = subprocess.Popen(command.split(),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        return (p.communicate()[0].decode())

    def list(self, reference=''):
        return 'Any(?) system command'