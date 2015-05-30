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
        try:
            return eval(self.substitute_placeholders(self.expression, parameters))
        except Exception as e:
            return 'ConditionalNode exception: id: %s, expression: %s, parameters: %s, exception: %s' % self.id, str(
                self.expression), str(self.parameters), str(e)

    def node_exec(self, parameters, async=False):
        q = Queue()
        res = self.action(parameters)
        logging.debug('For expression // ' + self.expression + ' // evaluation result is ' + str(res))
        selected_direction = self.yes if res else self.no
        res = bool(res)
        q.put((res, self.next if hasattr(self, 'next') else []))
        return q, selected_direction

    def execute(self, parameters):
        return self.node_exec(parameters, async=False)