import logging

__author__ = 'Кирилл'
import sqlite3

class Configuration():

    def __init__(self):
        self.__connect()

    connection = None
    cur = None

    def __connect(self):
        self.connection = sqlite3.connect('config.db', detect_types=sqlite3.PARSE_COLNAMES)
        self.cur = self.connection.cursor()

    def add_process(self, name, definition, runoninit=None):
        definition = definition.replace('\'', '\'\'')
        roi = ",'" + runoninit + "'" if runoninit else ', NULL'
        r = "INSERT INTO process (name, definition, runoninit) VALUES('"+name+"', '"+definition+"'"+roi+")"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        self.connection.commit()

    def update_process(self, name, definition):
        definition = definition.replace('\'', '\'\'')
        r = "UPDATE process SET definition='"+definition+"' WHERE name='"+name+"'"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        self.connection.commit()

    def delete_process(self, name):
        r = "DELETE FROM process WHERE name='"+name+"'"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        self.connection.commit()

    def get_process(self, name):
        r = "SELECT definition FROM process WHERE name='"+name+"'"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        definition = self.cur.fetchone()
        return definition

    def get_all_processes(self):
        r = "SELECT name, definition, runoninit FROM process"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        return [{'name': r[0], 'definition': r[1], 'runoninit': r[2]} for r in self.cur.fetchall()]

    def add_task(self, name, scheme, runned):
        r = "INSERT INTO task VALUES('"+name+"', '"+str(scheme)+"', '"+str(runned)+"')"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        self.connection.commit()

    def update_task(self, name, scheme, runned):
        r = "UPDATE task SET scheme='"+str(scheme)+"', runned='"+str(runned)+"' WHERE name='"+name+"'"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        self.connection.commit()

    def delete_task(self, name):
        r = "DELETE FROM task WHERE name='"+name+"'"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        self.connection.commit()

    def get_task(self, name):
        r = "SELECT scheme, runned FROM task WHERE name='"+name+"'"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        scheme = self.cur.fetchone()
        return scheme

    def get_all_tasks(self):
        r = "SELECT name, scheme, runned FROM task"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        return [{'name': r[0], 'scheme': r[1], 'runned': True if r[2] == 'True' else False} for r in self.cur.fetchall()]

    def get_all_plugins(self):
        r = "SELECT name, params, enabled FROM plugin"
        logging.info('SQL_conf: '+r)
        self.cur.execute(r)
        return [{'name': r[0], 'params': r[1], 'enabled': True if r[2] == 'True' else False} for r in self.cur.fetchall()]

    def update_plugin(self, name, params, enabled):
        r = "UPDATE plugin SET params=?, enabled=? where name=?"
        logging.info('SQL_conf: '+r+' # parameters: params='+params+' # enabled='+enabled)
        self.cur.execute(r, (params, enabled, name))
        self.connection.commit()

    def delete_plugin(self, name):
        r = "DELETE plugin where name=?"
        logging.info('SQL_conf: '+r+' # name='+name)
        self.cur.execute(r, (name))
        self.connection.commit()
