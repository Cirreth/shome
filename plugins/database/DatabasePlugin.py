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
        host = params['host']
        database = params['database']
        login = params['login']
        password = params['password']
        self._host = host
        self._database = database
        self._login = login
        self._password = password
        logging.debug('Database initialization')
        self._connection = pymysql.connect(host=host, user=login, passwd=password, db=database)
        self._connection.autocommit(True)
        self._cursor = self._connection.cursor(pymysql.cursors.DictCursor)
        #check
        self.call('select version()')

    def call(self, reference, values={}):
        return self.execute(reference)

    def execute(self, request):
        logging.debug('SQL: ( '+request+' )')
        try:
            self._cursor = self._connection.cursor(pymysql.cursors.DictCursor)
            self._cursor.execute(request)
        except pymysql.OperationalError:
            logging.warning('Reconnecting to database '+self._host+' : '+self._database)
            self._connection._connect(host=self._host, user=self._login, passwd=self._password, db=self._database)
            self._cursor = self._connection.cursor(pymysql.cursors.DictCursor)
            self._cursor.execute(request)
        return str(self._cursor.fetchall())

    def list(self, reference=''):
        raise NotImplementedError
