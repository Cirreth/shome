import logging

__author__ = 'cirreth'

import json
from core.entities import Base
from core.actproctree.AbstractNode import AbstractNode
from sqlalchemy import Column, String, Boolean


class Scenario(Base):
    __tablename__ = 'scenarios'

    _action_processor = None
    _config = None

    name = Column('name', String(32), primary_key=True)
    description = Column('description', String(255))
    expression = Column('expression', String(16000))
    runoninit = Column('runoninit', Boolean)
    published = Column('published', Boolean)

    def __init__(self, name, expression, description='', runoninit=False, published=False):
        #stored
        self.name = name
        self.expression = expression
        self.description = description
        self.runoninit = runoninit
        self.published = published
        #runtime
        self.variables = dict()
        self.isrunned = False
        self.root = []
        self.nodes = {}

    def construct(self):
        self.root = []
        struct = json.loads(self.expression)
        struct = {node['id']: node for node in struct}
        self.root = struct['Start'].next
        del struct['Start']
        self.nodes = {node['id']: AbstractNode(struct[node]) for node in struct}

    def execute(self, parameters):
        for root_node in self.root:
            node = self.nodes[root_node]
            result = node.execute(parameters)

        """
        {
          "id": "Start",
          "type": "StartNode",
          "next": [
            "rn144",
            "rn148"
          ],
          "parallel": [],
          "dimension": {
            "width": 90,
            "height": 32
          },
          "active": false
        }, {
          "id": "rn144",
          "type": "RequestNode",
          "plugin": "mock",
          "reference": "right",
          "position": {
            "left": 360,
            "top": 175
          },
          "next": [],
          "parallel": [],
          "exceptional": [],
          "dimension": {
            "width": 180,
            "height": 65
          },
          "active": false,
          "retvar": "b"
        }, {
          "id": "rn148",
          "type": "RequestNode",
          "plugin": "mock",
          "reference": "left",
          "position": {
            "left": 152,
            "top": 175
          },
          "next": [],
          "parallel": [],
          "exceptional": [],
          "dimension": {
            "width": 180,
            "height": 65
          },
          "active": false,
          "retvar": "a"
        }
        """

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