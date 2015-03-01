__author__ = 'Кирилл'

import json
from core.entities import Base
from sqlalchemy import Column, String, Boolean, ForeignKey

class Task(Base):
    __tablename__ = 'tasks'

    _config = None

    name = Column('name', String(32), primary_key=True)
    description = Column('description', String(255))
    scenario = Column('scenario', ForeignKey("scenarios.name"), nullable=False)
    type = Column('type', String(10), nullable=False)
    scheme = Column('scheme', String(8192), nullable=False)
    enabled = Column('enabled', Boolean, nullable=False)

    def __init__(self, name, scenario, task_type, scheme, enabled=False, description=""):
        self.name = name
        self.scenario = scenario
        if task_type in ('runonce', 'interval', 'scheme'):
            self.type = task_type
        else:
            raise Exception('Invalid task type. Must be runonce, interval or scheme.')
        self.scheme = scheme
        self.enabled = enabled
        self.description = description

    def __repr__(self):
        return json.dumps({
            'name': self.name,
            'description': self.description,
            'scenario': self.scenario,
            'type': self.type,
            'scheme': self.scheme,
            'enabled': self.enabled
        })

    def save(self):
        session = self._config.get_session()
        session.add(self)
        session.commit()

    def delete(self):
        session = self._config.get_session()
        session.delete(self)
        session.commit()

    @classmethod
    def get(cls, name):
        session = cls._config.get_session()
        return session.query(cls).get(name)