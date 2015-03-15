import json
from core.actproctree.RequestNode import RequestNode
from core.actproctree.DelayNode import DelayNode

__author__ = 'Кирилл'


class NodeBuilder:

    @classmethod
    def create_node(cls, structure):
        #structure = json.loads(expression)
        node_type = structure['type']
        if node_type == 'RequestNode':
            return RequestNode(structure)
        elif node_type == 'DelayNode':
            return DelayNode(structure)
