from queue import Queue
from core.processtree.NodeFactory import NodeFactory

__author__ = 'cirreth'

import json
import logging
from core.entities import Base
from core.processtree.Node import Node
from sqlalchemy import Column, String, Boolean, orm


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
        self.construct()

    @orm.reconstructor
    def __init_on_load(self):
        self.__init__(self, self.name, self.expression, self.description, self.runoninit, self.published)

    def construct(self):
        self.root = []
        struct = json.loads(self.expression)
        struct = {node['id']: node for node in struct}
        self.root = struct['Start']['next']
        del struct['Start']
        self.nodes = {node:  NodeFactory.create(struct[node]) for node in struct}

    def execute(self, parameters):
        result = {}
        parallel = Queue()
        first_iteration = True
        while first_iteration or not parallel.empty():
            first_iteration = False
            queues = {}
            next_nodes = []
            # preparing queue
            for node in self.root:
                parallel.put(node)
            # execute all parallel
            while not parallel.empty():
                node = parallel.get()
                queues[self.nodes[node].id], nodes_parallel = self.nodes[node].execute(parameters)
                for prl in nodes_parallel:
                    parallel.put(prl)
            # collect results
            for node_id, q in queues.items():
                res, node_next = q.get()
                next_nodes += node_next
                result.update(res if res else {})
            # execute all next_nodes
            for node in next_nodes:
                parallel.put(node)
        return result

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
        return self

    def delete(self):
        session = self._config.get_session()
        session.delete(self)
        session.commit()

    @classmethod
    def get(cls, name):
        session = cls._config.get_session()
        return session.query(cls).get(name)