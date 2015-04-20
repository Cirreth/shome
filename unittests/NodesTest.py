import json
import logging
import unittest
import time
from core.Database import Database
from core.PluginManager import PluginManager
from core.actproctree.Node import Node

logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')


class NodesTest(unittest.TestCase):

    cfg = Database()
    pm = PluginManager()
    pm._config = cfg

    def test_request_node(self):
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
        node = Node.create(structure)
        self.assertEqual(node.plugin, 'mock')
        self.assertEqual(node.reference, 'right')

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
        node = Node.create(structure)
        start_time = time.time()
        node.execute({})
        elapsed_time = time.time() - start_time
        self.assertGreater(0.5, abs(elapsed_time-timeconst))

    def test_required_fields(self):
        bad_node = """
            {
                "type": "RequestNode"
            }
        """
        bn_structure = json.loads(bad_node)
        self.assertRaises(Exception, Node.create, bn_structure)
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
        self.assertRaises(Exception, Node.create, brn_structure)
