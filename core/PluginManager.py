from core.processtree.RequestNode import RequestNode

__author__ = 'cirreth'
from core.entities.Plugin import Plugin


class PluginManager:

    _plugins = {}

    def __init__(self):
        RequestNode.set_plugin_manager(self)
        self.__reload_all_configured()

    def __reload_all_configured(self):
        # @TODO UNLOAD ALL PLUGINS BEFORE LOAD NEW
        self._plugins = {p.instname: p for p in Plugin.get_all()}

    def call_plugin(self, name, reference, values={}):
        return self._plugins[name].call(reference, values)

    def list_all(self):
        return {instname: plugin.dict() for instname, plugin in self._plugins.items()}