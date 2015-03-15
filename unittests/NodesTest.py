import json
import os
import logging
import unittest
import time
from core.actproctree.NodeBuilder import NodeBuilder

logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')


class NodesTest(unittest.TestCase):

    def test_request_node(self):
        expression = """
            {
                "id": "rn144",
                "type": "RequestNode",
                "plugin": "mock",
                "reference": "right",
                "position": {
                    "left": 360,
                    "top": 175
                }
            }
        """
        structure = json.loads(expression)
        node = NodeBuilder.create_node(structure)

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
        node = NodeBuilder.create_node(structure)
        start_time = time.time()
        node.execute({})
        elapsed_time = time.time() - start_time
        self.assertGreater(0.5, abs(elapsed_time-2))

    def test_required_fields(self):
        bad_node = """
            {
                "type": "RequestNode"
            }
        """
        bn_structure = json.loads(bad_node)
        self.assertRaises(Exception, NodeBuilder.create_node, bn_structure)
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
        self.assertRaises(Exception, NodeBuilder.create_node, brn_structure)
