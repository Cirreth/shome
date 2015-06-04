from plugins.SHomePlugin import SHomePlugin
import logging
import sqlite3
import os


class MemoryPlugin(SHomePlugin):

    def __init__(self, params):
        self._filename = params['filename'] if 'filename' in params else 'memory.db'
        try:
            if self._filename in os.listdir(''):
                self._connection = self.__create_database()
            self._connection = sqlite3.connect('memory.db')
        except sqlite3.Error as e:
            logging.error('Memory database initalization error: '+str(e))
            raise e

    def __create_database(self):
        try:
            conn = sqlite3.connect(self._filename)
            cur = conn.cursor()
            cur.execute('CREATE TABLE memory (parameter TEXT PRIMARY KEY, value TEXT)')
            cur.commit()
        except Exception as e:
            logging.error('Error on database create: '+str(e))
            raise e
        return conn

    def _read(self, parameter):
        cur = self._connection.cursor()
        rs = cur.execute('SELECT value FROM memory WHERE parameter = ?', (parameter,))
        return rs.fetchone()[0]

    def _write(self, parameter, value):
        try:
            cur = self._connection.cursor()
            cur.execute('INSERT OR REPLACE INTO memory (parameter, value) VALUES (?, ?)', (parameter, value, ))
            cur.commit()
        except Exception as e:
            cur.rollback()
            logging.error('Error on write in memory plugin operation: '+ str(e))
            raise e

    def call(self, reference, value=None):
        if value is not None:
            self._write(reference, value)
        else:
            return self._read(reference)

    def list(self, reference=''):
        return 'Name || Name & value'