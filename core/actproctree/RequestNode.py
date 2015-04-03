__author__ = 'cirreth'

import logging
from core.actproctree.Node import Node

class RequestNode(Node):
    """Request value from plugin"""

    _plugin_manager = None
    _required_fields = ['reference', 'plugin']
    _optional_fields = ['retvar', 'value']

    def __init__(self, structure):
        if not RequestNode._plugin_manager:
            raise Exception("""Setup RequestNode._plugin_manager variable before initializing node instances.\n
                            Use method .set_plugin_manager""")
        super().__init__(structure)

    def action(self, parameters):
        res = self._plugin_manager.call_plugin(self.plugin, self.reference, parameters)
        if hasattr(self, 'retvar'):
            return {self.retvar: res}

    @classmethod
    def set_plugin_manager(cls, plugin_manager):
        cls._plugin_manager = plugin_manager
