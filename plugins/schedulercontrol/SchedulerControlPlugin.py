import logging
from plugins.SHomePlugin import SHomePlugin

__author__ = 'Кирилл'

class SchedulerControlPlugin(SHomePlugin):

    _scheduler = None

    def __init__(self, parameters):
        raise NotImplementedError('It is necessary to integrate it module in core')

    def call(self, reference, values={}):
        logging.info('Scheduler control plugin'+reference)
        if reference.find('start ') == 0:
            self._scheduler.start(reference[6:])
        elif reference.find('stop ') == 0:
            self._scheduler.stop(reference[5:])
        elif reference.find('scheme ') == 0:
            tail = reference[7:]
            splt = tail.find(' ')
            self._scheduler.setscheme(tail[splt:], tail[:splt])

    def list(self, reference=''):
        return str(self._action_processor.pss_variables.keys())
