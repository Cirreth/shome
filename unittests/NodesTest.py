import json
import logging
import unittest
import time

from core.Database import Database
from core.PluginManager import PluginManager
from core import NodeFactory
from core.processtree.Node import Node


logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')


class NodesTest(unittest.TestCase):

    cfg = Database()
    pm = PluginManager()
    pm._config = cfg

    def test_request_node_parsing(self):
        expression = """
            {
                "id": "rn144",
                "type": "RequestNode",
                "plugin": "mock",
                "reference": "right",
                "retvar": "res",
                "position": {
                    "left": 360,
                    "top": 175
                }
            }
        """
        structure = json.loads(expression)
        node = NodeFactory.create(structure)
        self.assertEqual(node.plugin, 'mock')
        self.assertEqual(node.reference, 'right')

    def test_request_node_exec(self):
        expression = """
            {
                "id": "rn144",
                "type": "RequestNode",
                "plugin": "mock",
                "reference": "right",
                "retvar": "res",
                "position": {
                    "left": 360,
                    "top": 175
                }
            }
        """
        structure = json.loads(expression)
        node = NodeFactory.create(structure)
        q, parallel = node.execute({})
        res, next = q.get()
        self.assertEqual(parallel, [])
        self.assertEqual(next, [])
        self.assertEqual(res, {'res': 'right'})

    def test_delay_node(self):
        timeconst = 2
        expression = """
            {
              "id": "rn36",
              "type": "DelayNode",
              "delay": %d,
              "position": {
                "left": 292,
                "top": 160
              },
              "next": [],
              "parallel": [],
              "exceptional": []
            }
        """ % timeconst
        structure = json.loads(expression)
        node = NodeFactory.create(structure)
        start_time = time.time()
        node.execute({})
        elapsed_time = time.time() - start_time
        self.assertGreaterEqual(timeconst, abs(elapsed_time-timeconst))

    def test_required_fields(self):
        bad_node = """
            {
                "type": "RequestNode"
            }
        """
        bn_structure = json.loads(bad_node)
        self.assertRaises(Exception, NodeFactory.create, bn_structure)
        bad_request_node = """
            {
                "id": "test",
                "type": "RequestNode",
                "position": {
                    "x": 0,
                    "y": 0
                }
            }
        """
        brn_structure = json.loads(bad_request_node)
        self.assertRaises(Exception, NodeFactory.create, brn_structure)

    def test_conditional_node(self):
        expression = """
            {
                "id": "test",
                "type": "ConditionalNode",
                "expression": "1+1",
                "yes": [],
                "no": [],
                "position": {
                    "x": 0,
                    "y": 0
                }
            }
        """
        structure = json.loads(expression)
        node = NodeFactory.create(structure)
        q, parallel = node.execute({})
        res, next = q.get()
        self.assertEqual(res, True)
        # replace expression and run next test
        structure['expression'] = "1 === 2"
        node = NodeFactory.create(structure)
        q, parallel = node.execute({})
        res, next = q.get()
        self.assertEqual(res, False)

    def test_substitution(self):
        q1 = "[x] == 1"
        self.assertEqual(Node.substitute_placeholders(q1, {'x': 1}), '1 == 1')