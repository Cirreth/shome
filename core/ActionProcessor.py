__author__ = 'cirreth'

import logging
from core.entities.Scenario import Scenario


class ActionProcessor:

    def __init__(self):
        self._scenarios = {}

    def add_scenario(self, name, expression, description='', runoninit=False, published=False):
        if name in self._scenarios:
            raise Exception('Scenario with name '+name+' already exists')
        self._scenarios[name] = Scenario(name, expression, description, runoninit, published)

    def get_scenario(self, name):
        if name in self._scenarios:
            return self._scenarios[name]

    def delete_scenario(self, name):
        del self._scenarios[name]

    def execute(self, name, params={}):
        if not isinstance(params, dict):
            raise Exception('Parameters type must be dict')
        if name in self._scenarios:
            return self._scenarios[name].execute(params)

    def list_all(self):
        return [scenario.dict() for scenario in self._scenarios]