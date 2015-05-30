from plugins.SHomePlugin import SHomePlugin

__author__ = 'cirreth'

import logging


class MockPlugin(SHomePlugin):

    def call(self, reference, values={}):
        logging.debug('MockPlugin call with '+reference)
        return reference

    def list(self, reference=''):
        return 'Any value'