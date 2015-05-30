__author__ = 'cirreth'

from core.entities.Scenario import Scenario
from core.entities.Plugin import Plugin
from core.entities.Task import Task
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


class Database():

    def __init__(self):
        Scenario._config = self
        Plugin._config = self
        Task._config = self
        self._engine = create_engine('sqlite:///config.db', connect_args={'check_same_thread': False})
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        self._metadata = MetaData(bind=self._engine)

    def get_session(self):
        return self._session

    def create_database(self):
        Scenario.metadata.bind = self._engine
        Scenario.metadata.create_all()
        Plugin.metadata.bind = self._engine
        Plugin.metadata.create_all()
        Task.metadata.bind = self._engine
        Task.metadata.create_all()

