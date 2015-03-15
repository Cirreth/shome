from core.entities.Plugin import Plugin

__author__ = 'cirreth'


class PluginManager:

    _plugins = {}

    def __init__(self):
        self.__reload_all_plugins()

    def __reload_all_plugins(self):
        pass

    def call_plugin(self, name, reference, values={}):
        pass

    def list_all(self):
        return self._plugins.keys()