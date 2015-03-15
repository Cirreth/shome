from core.entities.Plugin import Plugin

__author__ = 'cirreth'


class PluginManager:
    """
    Plugin lifecycle:
        1. Found on scanning        -> 2
        2. Configured [and saved]   -> 3, 4
        3. Initialized (ready)      -> 4
        4. Unloaded                 -> 5
        5. Loaded from db           -> 3, 4
    """

    _plugins = {}

    def __init__(self):
        self.__reload_all_configured()

    def __reload_all_configured(self):
        #@TODO UNLOAD ALL PLUGINS
        self._plugins = {p.instname: p for p in Plugin.get_all()}

    def call_plugin(self, name, reference, values={}):
        pass

    def list_all(self):
        return list(self._plugins.keys())