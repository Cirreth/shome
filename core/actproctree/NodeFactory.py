__author__ = 'Кирилл'

from core.actproctree import *


class NodeFactory():

    @classmethod
    def create(cls, structure):
        node_type = structure['type']
        if node_type == 'RequestNode':
            return RequestNode(structure)
        elif node_type == 'DelayNode':
            return DelayNode(structure)