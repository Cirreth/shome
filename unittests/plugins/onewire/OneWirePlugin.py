__author__ = 'cirreth'

from libs import ownet
from plugins.SHomePlugin import SHomePlugin
import json
import logging

class OneWirePlugin(SHomePlugin):

    #static
    _READ_ATTEMPTS_COUNT = 3

    #
    _host = None
    _port = None
    _connection = None

    def __init__(self, parameters):
        params = json.loads(parameters)
        self._host = params['host']
        self._port = int(params['port'])
        logging.debug('OneWirePlugin initialization')
        self._connection = ownet.Connection(self._host, self._port)
        logging.debug('\nOneWirePlugin list dir:')
        for d in self._connection.dir(''):
            logging.debug(d)
        logging.debug('\n')

    def _read(self, address):
        attempt = 0
        logging.debug('OneWirePlugin read address '+str(address)+' (attempt: '+str(attempt)+')')
        while attempt < self._READ_ATTEMPTS_COUNT:
            try:
                if address.find('dir ') == 0:
                    return str(self.list(address[5:]))
                res = self._connection.read(address)
                break
            except Exception as e:
                attempt += 1
                res = 'Exception occured: ' + str(e)
        logging.debug('OneWirePlugin address '+address+' reading result : '+str(res))
        return res

    def _write(self, address, value):
        logging.debug('OneWirePlugin trying to write address ( '+address+' ) and value ( '+str(value)+' )...')
        res = self._connection.write(address, value)
        logging.debug('OneWirePlugin have writen value ' + str(value) + ' to address '+address+' with result : '+str(res))

    def call(self, reference, value=None):
        if value is not None:
            return self._write(reference, value)
        else:
            return self._read(reference)

    def list(self, reference=''):
        dir = self._connection.dir(reference)
        res = []
        for d in dir:
            res.append(d.decode())
        return res