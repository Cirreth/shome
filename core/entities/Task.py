import logging
import threading

__author__ = 'Кирилл'

import json
from core.entities import Base
from sqlalchemy import Column, String, Boolean, ForeignKey, orm

class Task(Base):
    __tablename__ = 'tasks'

    _config = None
    _action_processor = None

    # stored
    name = Column('name', String(32), primary_key=True)
    description = Column('description', String(255))
    scenario = Column('scenario', ForeignKey("scenarios.name"), nullable=False)
    type = Column('type', String(10), nullable=False)
    scheme = Column('scheme', String(8192), nullable=False)
    enabled = Column('enabled', Boolean, nullable=False)

    # runtime

    # scheduled infrequent tasks. {name: next_run}
    _scheduled = {}

    def __init__(self, name, scenario, task_type, scheme, enabled=False, description=""):
        self.name = name
        self.scenario = scenario
        if task_type in ('runonce', 'interval', 'scheme'):
            self.type = task_type
        else:
            raise Exception('Invalid task type. Must be runonce, interval or scheme.')
        self.scheme = scheme
        self._scheme = json.loads(scheme)
        self.enabled = enabled
        self.description = description
        self._started = False

    @orm.reconstructor
    def __init_on_load(self):
        self.__init__(self.name, self.scenario, self.type, self.scheme, self.enabled, self.description)
        if self.enabled:
            self.start(save=False)

    def set_scheme(self, scheme):
        self.scheme = scheme
        self._scheme = json.loads(scheme)

    def dict_repr(self):
        return {
            'name': self.name,
            'description': self.description,
            'scenario': self.scenario,
            'type': self.type,
            'scheme': self.scheme,
            'enabled': self.enabled
        }

    def _start_frequent_interval(self):
        def tick(first=False):
            if not first:
                self._action_processor.execute(self.scenario)
            t = threading.Timer(self._scheme['interval'], tick)
            t.start()
            return t
        self._thread = tick(True)

    def start(self, save=True):
        if self._started:
            return False
        try:
            if self.type == 'interval' and self._scheme['interval'] < 300:
                self._start_frequent_interval()
            elif self.type == 'interval' and self._scheme['interval'] >= 300:
                raise NotImplementedError()
            elif self.type == 'runonce':
                raise NotImplementedError()
            elif self.type == 'scheme':
                raise NotImplementedError()
            self._started = True
            try:
                if save:
                    self.save()
            except Exception as e:
                logging.error('Error on saving task state: '+str(e))
        except Exception as e:
            logging.error(str(e))
            return False
        return True

    def stop(self, save=True):
        if not self._started:
            return False
        try:
            if self.type == 'interval' and self._scheme['interval'] < 300:
                self._thread.cancel()
            elif self.type == 'interval' and self._scheme['interval'] >= 300:
                raise NotImplementedError()
            elif self.type == 'runonce':
                raise NotImplementedError()
            elif self.type == 'scheme':
                raise NotImplementedError()
            try:
                self._started = False
                if save:
                    self.save()
            except Exception as e:
                logging.error('Error on saving task state: '+str(e))
        except Exception as e:
            logging.error('Error on task state changing: '+str(e))
            return False
        return True

    def save(self):
        session = self._config.get_session()
        try:
            session.add(self)
            session.commit()
            return self
        except Exception as e:
            logging.error('Exception occurs in method save of '+self.name+' task: '+str(e))
            session.rollback()
            raise e

    def delete(self):
        session = self._config.get_session()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            logging.error('Exception occurs in method delete of '+self.name+' task: '+str(e))
            session.rollback()
            raise e

    @classmethod
    def get(cls, name):
        session = cls._config.get_session()
        return session.query(cls).get(name)

    @classmethod
    def get_all(cls):
        session = cls._config.get_session()
        return session.query(cls).all()