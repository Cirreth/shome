__author__ = 'cirreth'

import json
from core.entities import Base
from sqlalchemy import Column, String, Boolean


class Plugin(Base):
    __tablename__ = 'plugins'

    _config = None

    instname = Column('instname', String(32), primary_key=True)
    name = Column('name', String(32))
    _params = Column('params', String(16000))
    enabled = Column('enabled', Boolean)

    def __init__(self, instname, name, params='{}', enabled=True):
        #stored
        self.name = name
        self.instname = instname
        self._params = params
        self.enabled = enabled
        #runtime
        self._params_dict = dict()
        self.plugin_instance = None

    def set_parameter(self, name, value: "None to delete parameter"):
        if value:
            self._params_dict[name] = value
        else:
            del self._params_dict[name]
        self._params = json.dumps(self._params_dict)

    def get_params(self):
        return self._params_dict

    def __repr__(self):
        return json.dumps({
            'instname': self.instname,
            'name': self.name,
            'params': self._params,
            'enabled': self.enabled,
            'state': self.state
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
    def get(cls, instname):
        session = cls._config.get_session()
        return session.query(cls).get(instname)

    @classmethod
    def get_all(cls):
        session = cls._config.get_session()
        return session.query(cls).all()