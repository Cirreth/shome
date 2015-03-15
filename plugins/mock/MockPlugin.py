__author__ = 'cirreth'

import logging
from core.entities.Plugin import Plugin


class MockPlugin(Plugin):

    def call(self, reference, values={}):
        logging.debug('MockPlugin call with '+reference)
        return reference

    def list(self, reference=''):
        return 'Any value'