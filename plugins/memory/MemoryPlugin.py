from plugins.SHomePlugin import SHomePlugin
import logging
import sqlite3
import os


class MemoryPlugin(SHomePlugin):

    def __init__(self, params):
        self._filename = params['filename'] if 'filename' in params else 'memory.db'
        try:
            if self._filename not in os.listdir('.'):
                self._connection = self.__create_database()
            self._connection = sqlite3.connect('memory.db', check_same_thread=False)
        except sqlite3.Error as e:
            logging.error('Memory database initalization error: '+str(e))
            raise e

    def __create_database(self):
        conn = sqlite3.connect(self._filename, check_same_thread=False)
        cur = conn.cursor()
        cur.execute('CREATE TABLE memory (parameter TEXT PRIMARY KEY, value TEXT)')
        conn.commit()
        return conn

    def _read(self, parameter):
        cur = self._connection.cursor()
        rs = cur.execute('SELECT value FROM memory WHERE parameter = ?', (parameter,))
        res = rs.fetchone()
        return res[0] if res else ''

    def _write(self, parameter, value):
        try:
            cur = self._connection.cursor()
            cur.execute('INSERT OR REPLACE INTO memory (parameter, value) VALUES (?, ?)', (parameter, value, ))
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            logging.error('Error on write in memory plugin operation: '+str(e))
            raise e

    def call(self, reference, value=None):
        if value is not None and value != '':
            self._write(reference, value)
        else:
            return self._read(reference)

    def list(self, reference=''):
        return 'Name || Name & value'