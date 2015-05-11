__author__ = 'cirreth'

import logging
from core.entities.Scenario import Scenario


class ActionProcessor:

    def __init__(self, load_stored=True):
        if load_stored:
            self._scenarios = {scenario.name: scenario for scenario in Scenario.get_all()}
        else:
            self._scenarios = {}

    def add_scenario(self, name, expression, description='', runoninit=False, published=False, save=False):
        if name in self._scenarios:
            raise Exception('Scenario with name '+name+' already exists')
        self._scenarios[name] = Scenario(name, expression, description, runoninit, published)
        if save:
            self._scenarios[name].save()

    def update_scenario(self, name, expression, description='', runoninit=False, published=False):
        if name not in self._scenarios:
            raise Exception(name+' is not in scenarios')
        scenario = self._scenarios[name]
        scenario.expression = expression
        scenario.description = description
        scenario.runoninit = runoninit
        scenario.published = published
        scenario.save()

    def get_scenario(self, name):
        if name in self._scenarios:
            return self._scenarios[name]

    def delete_scenario(self, name):
        scenario = Scenario.get(name)
        if scenario:
            scenario.delete()
        del self._scenarios[name]

    def execute(self, name, params={}):
        if not isinstance(params, dict):
            raise Exception('Parameters type must be dict')
        if name in self._scenarios:
            return self._scenarios[name].execute(params)

    def list_all(self):
        return self._scenarios.items()