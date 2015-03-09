__author__ = 'cirreth'

import logging
from core.actproctree.AbstractNode import AbstractNode


class RequestNode(AbstractNode):
    """Request value from plugin"""

    _required_fields = ['reference']

    def __init__(self, structure):
        super().__init__(structure)

    def action(self, parameters):
        return 100500