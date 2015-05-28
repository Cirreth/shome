import logging
from queue import Queue
from execjs import eval

__author__ = 'cirreth'
from core.processtree.Node import Node


class ConditionalNode(Node):
    """Evaluate condition then execute "yes" or "no" branch"""

    _required_fields = ['expression', 'yes', 'no']
    _optional_fields = []

    def __init__(self, structure):
        super().__init__(structure)

    def action(self, parameters):
        return eval(self.substitute_placeholders(self.expression, parameters))

    def node_exec(self, parameters, async=False):
        q = Queue()
        res = self.action(parameters)
        logging.debug('For expression // '+self.expression+' // evaluation result is '+str(res))
        direction_next = self.yes if res else self.no
        res = bool(res)
        q.put((res, direction_next))
        return q, self.parallel if 'parallel' in self._directions else []

    def execute(self, parameters):
        return self.node_exec(parameters, async=False)