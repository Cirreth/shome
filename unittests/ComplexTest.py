import json
import logging
from queue import Queue
import unittest
import time
from core.Database import Database
from core.PluginManager import PluginManager
from core.processtree.Node import Node
from core.processtree.NodeFactory import NodeFactory

logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')


class NodesTest(unittest.TestCase):

    cfg = Database()
    pm = PluginManager()
    pm._config = cfg

    def test_ow_plugin_loading(self):
        self.assertIn('onewire', self.pm.list_all())

    def test_ow_execution(self):
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