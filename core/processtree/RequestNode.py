__author__ = 'cirreth'
from core.processtree.Node import Node


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
        value = self.value if hasattr(self, 'value') else None
        reference = Node.substitute_placeholders(self.reference, parameters)
        res = self._plugin_manager.call_plugin(self.plugin, reference, value)
        if hasattr(self, 'retvar'):
            return {self.retvar: res}

    def execute(self, parameters):
        return self.node_exec(parameters, async=True)

    @classmethod
    def set_plugin_manager(cls, plugin_manager):
        cls._plugin_manager = plugin_manager
