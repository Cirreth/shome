__author__ = 'cirreth'

import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean

Base = declarative_base()


class Scenario(Base):
    __tablename__ = 'scenario'

    _action_processor = None
    _config = None

    name = Column('name', String(16), primary_key=True)
    description = Column('description', String(128))
    expression = Column('expression', String(16000))
    runoninit = Column('runoninit', Boolean)
    published = Column('published', Boolean)

    def __init__(self, name, expression, description='', runoninit=False, published=False):
        self.name = name
        self.expression = expression
        self.description = description
        self.runoninit = runoninit
        self.published = published
        self.variables = dict()
        self.running = False

    def execute(self, params):
        raise NotImplementedError()

    def __repr__(self):
        return json.dumps({
            'name': self.name,
            'description': self.description,
            'expression': self.expression,
            'runOnInit': self.runoninit,
            'published': self.published
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