import logging
import threading
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
    task_type = Column('type', String(10), nullable=False)
    scheme = Column('scheme', String(8192), nullable=False)
    enabled = Column('enabled', Boolean, nullable=False)

    # runtime

    # scheduled infrequent tasks. {name: next_run}
    _scheduled = {}

    def __init__(self, name, scenario, task_type, scheme, enabled=False, description=""):
        self.name = name
        self.scenario = scenario
        if task_type in ('runonce', 'interval', 'scheme'):
            self.task_type = task_type
        else:
            raise Exception('Invalid task type. Must be runonce, interval or scheme.')
        self.scheme = json.dumps(scheme)
        self._scheme = scheme
        self.enabled = enabled
        self.description = description
        self._started = False
        if self.enabled:
            self.start(save=False)

    @orm.reconstructor
    def __init_on_load(self):
        self.__init__(self.name, self.scenario, self.task_type, json.loads(self.scheme), self.enabled, self.description)

    def set_scheme(self, scheme):
        if scheme is None:
            return
        self.scheme = json.dumps(scheme)
        self._scheme = scheme

    def dict_repr(self):
        return {
            'name': self.name,
            'description': self.description,
            'scenario': self.scenario,
            'type': self.task_type,
            'scheme': self._scheme,
            'enabled': self.enabled
        }

    def _start_frequent_interval(self):
        def tick(first=False):
            if not first:
                try:
                    if not self._started:
                        logging.warning('Thread of task '+self.name+' was cancelled, but it continues executing')
                        return
                    self._action_processor.execute(self.scenario)
                except Exception as e:
                    logging.error('Exception in _start_frequent_interval task ('+self.name+'): '+str(e))
            t = threading.Timer(self._scheme['interval'], tick)
            t.start()
            return t
        self._thread = tick(True)

    def start(self, save=True):
        if self._started:
            raise Exception('Already started')
        try:
            if self.task_type == 'interval' and self._scheme['interval'] < 1000:
                self._start_frequent_interval()
                logging.debug('Frequent task with name '+self.name+' initialized')
            elif self.task_type == 'interval' and self._scheme['interval'] >= 300:
                raise NotImplementedError('Not implemented yet')
            elif self.task_type == 'runonce':
                raise NotImplementedError('Not implemented yet')
            elif self.task_type == 'scheme':
                raise NotImplementedError('Not implemented yet')
            self._started = True
            try:
                if save:
                    self.save()
            except Exception as e:
                logging.error('Error on saving task state: '+str(e))
        except Exception as e:
            logging.error('Unknown error on task initialization: '+str(e))
            return False
        return True

    def stop(self, save=True):
        if not self._started:
            raise Exception('Already stopped')
        try:
            if self.task_type == 'interval' and self._scheme['interval'] < 300:
                self._thread.cancel()
            elif self.task_type == 'interval' and self._scheme['interval'] >= 300:
                raise NotImplementedError()
            elif self.task_type == 'runonce':
                raise NotImplementedError()
            elif self.task_type == 'scheme':
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
            session.rollback()
            logging.error('Exception occurs in method save of '+self.name+' task: '+str(e))
            raise e

    def delete(self):
        session = self._config.get_session()
        try:
            if self._started:
                self.stop()
            session.delete(self)
            session.commit()
        except Exception as e:
            logging.error('Exception occurs in method delete of '+self.name+' task: '+str(e))
            session.rollback()
            raise e

    @classmethod
    def check_scheme(cls, task_type, scheme):
        """
        Not implemented
        :return:
        """
        return True

    @classmethod
    def get(cls, name):
        session = cls._config.get_session()
        return session.query(cls).get(name)

    @classmethod
    def get_all(cls):
        session = cls._config.get_session()
        return session.query(cls).all()