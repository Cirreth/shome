__author__ = 'cirreth'

from plugins.SHomePlugin import SHomePlugin
import logging
import json
import pymysql

class DatabaseMySQLPlugin(SHomePlugin):

    _host = None
    _login = None
    _password = None
    _database = None

    _connection = None
    _cursor = None

    def __init__(self, parameters):
        params = json.loads(parameters)
        self._host = params['host']
        self._database = params['database']
        self._login = params['login']
        self._password = params['password']
        logging.debug('Database initialization')
        self.__connect()

    def call(self, reference, values={}):
        return self.execute(reference)

    def execute(self, request):
        logging.debug('SQL: ( '+request+' )')
        try:
            self._cursor = self._connection.cursor(pymysql.cursors.DictCursor)
            logging.debug('Request result: '+str(self._cursor.execute(request)))
        except pymysql.OperationalError:
            logging.warning('Connecting to database '+self._host+' : '+self._database)
            self.__connect()
            self._cursor.execute(request)
        try:
            return str(self._cursor.fetchall())
        except Exception as e:
            return str(e)

    def __connect(self):
        self._connection = pymysql.connect(host=self._host, user=self._login, passwd=self._password, db=self._database)
        self._connection.autocommit(True)
        self._cursor = self._connection.cursor(pymysql.cursors.DictCursor)

    def list(self, reference=''):
        raise NotImplementedError
