__author__ = 'cirreth'

from plugins.SHomePlugin import SHomePlugin
import logging
import time


class DelayPlugin(SHomePlugin):

    def __init__(self, parameter):
        pass

    def call(self, reference, values={}):
        logging.info('Delay '+reference)
        time.sleep(float(reference))

    def list(self, reference=''):
        return 'Delay interval in seconds'