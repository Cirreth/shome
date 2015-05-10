__author__ = 'cirreth'
import importlib
import os
import json
from core.entities import Base
from sqlalchemy import Column, String, Boolean, orm


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
        self.state = 'active'
        self._params_dict = None
        self.plugin_instance = None
        #init
        self.__update_dict_repr()
        self.__load()

    @orm.reconstructor
    def __init_on_load__(self):
        self.__init__(self.instname, self.name, self._params, self.enabled)

    def call(self, reference, values):
        return self.plugin_instance.call(reference, values)

    def __load(self):
        for name in os.listdir('./plugins/'+self.name):
            if not name.startswith('__') and name.endswith('.py'):
                mdl = importlib.import_module('plugins.'+self.name+'.'+name[:-3])
                plg = getattr(mdl, name[:-3])
                self.plugin_instance = plg(self._params_dict)

    def __update_str_repr(self):
        self._params = json.dumps(self._params_dict)

    def __update_dict_repr(self):
        self._params_dict = json.loads(self._params)

    def set_param(self, name, value):
        self._params_dict[name] = value
        self.__update_str_repr()

    def del_param(self, param):
        if param in self._params_dict:
            del self._params_dict[param]
            self.__update_str_repr()

    def get_param(self, param):
        if param in self._params_dict:
            return self._params_dict[param]
        else:
            return None

    def get_params(self):
        return self._params_dict

    def dict(self):
        return {
            'instname': self.instname,
            'name': self.name,
            'params': self._params,
            'enabled': self.enabled,
            'state': self.state
        }

    def __repr__(self):
        return json.dumps(self.json_repr())

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
    def get(cls, instname):
        session = cls._config.get_session()
        return session.query(cls).get(instname)

    @classmethod
    def get_all(cls):
        session = cls._config.get_session()
        return session.query(cls).all()