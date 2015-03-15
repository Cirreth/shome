__author__ = 'cirreth'

from core.actproctree import *
from threading import Thread
import json
import re
import logging
from core.entities.Scenario import Scenario


class ActionProcessor:

    def __init__(self):
        pass

    def init(self, context):
        logging.info("Action processor initialization")
        Scenario._action_processor = self
        Scenario._config = context.config
        self._config = context.config

    def add_scenario(self, name, expression, description='', runoninit=False, published=False):
        if name in self._scenarios:
            raise Exception('Scenario with name '+name+' already exists')
        self._scenarios[name] = Scenario(name, expression, description, runoninit, published)

    def get_scenario(self, name):
        if name in self._scenarios:
            return self._scenarios[name]

    def delete_scenario(self, name):
        raise NotImplementedError()

    def execute(self, name, params: "dict"):
        if isinstance(params, dict):
            raise Exception('Parameters type must be dict')
        if name in self._scenarios:
            return self._scenarios[name].execute()