__author__ = 'cirreth'

from core.entities.Scenario import Scenario
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


class Config():

    def __init__(self):
        Scenario._config = self
        self._engine = create_engine('sqlite:///config.db', echo=True)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        self._metadata = MetaData(bind=self._engine)

    def get_session(self):
        return self._session

    def create_database(self):
        Scenario.metadata.bind = self._engine
        Scenario.metadata.create_all()