import os
import logging
import unittest
from core.actproctree.NodeBuilder import NodeBuilder

logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')


class PerformerTest(unittest.TestCase):

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
        node = NodeBuilder.create_node(expression)
        print(node.execute({}))

    def test_delay_node(self):
        expression = """
            {
              "id": "rn36",
              "type": "DelayNode",
              "delay": 2,
              "position": {
                "left": 292,
                "top": 160
              },
              "next": [],
              "parallel": [],
              "exceptional": []
            }
        """
        node = NodeBuilder.create_node(expression)
        print(node.execute({}))

    def test_required_fields(self):
        bad_node = """
            {
                "type": "RequestNode"
            }
        """
        self.assertRaises(Exception, NodeBuilder.create_node, bad_node)
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
        self.assertRaises(Exception, NodeBuilder.create_node, bad_request_node)
