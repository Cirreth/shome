import json
import logging
from queue import Queue
import unittest
import time
from core.Database import Database
from core.PluginManager import PluginManager
from core.entities.Scenario import Scenario
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
        expression = r"""
            {
                "id": "rn144",
                "type": "RequestNode",
                "plugin": "onewire",
                "reference": "/28.F2CF39040000/temperature10",
                "retvar": "res",
                "position": {
                    "left": 360,
                    "top": 175
                }
            }
        """
        structure = json.loads(expression)
        node = NodeFactory.create(structure)
        self.assertEqual(node.plugin, 'onewire')
        self.assertEqual(node.reference, '/28.F2CF39040000/temperature10')
        res = node.execute({})[0].get()[0]
        self.assertGreater(float(res['res']), 10)

    def test_ow_scenario(self):
        expression = r"""
        [
            {
                "id": "Start",
                "type": "StartNode",
                "next": [
                    "rn144"
                ]
            },
            {
                "id": "rn144",
                "type": "RequestNode",
                "plugin": "onewire",
                "reference": "/28.F2CF39040000/temperature10",
                "retvar": "res",
                "position": {
                    "left": 360,
                    "top": 175
                }
            }
        ]
        """
        s = Scenario('demo', expression)
        res = s.execute({})
        self.assertGreater(res['res'], 10)

    def test_ow_scenario_write(self):
        val = 0
        expression = r"""
        [
            {
                "id": "Start",
                "type": "StartNode",
                "next": [
                    "rn144"
                ]
            },
            {
                "id": "rn144",
                "type": "RequestNode",
                "plugin": "onewire",
                "reference": "/3A.F2360D000000/PIO.A",
                "value": %d,
                "retvar": "rstate",
                "position": {
                    "left": 360,
                    "top": 175
                },
                "next": [
                    "rn145"
                ]
            },
            {
                "id": "rn145",
                "type": "RequestNode",
                "plugin": "onewire",
                "reference": "/3A.F2360D000000/PIO.A",
                "retvar": "res",
                "position": {
                    "left": 360,
                    "top": 175
                }
            }
        ]
        """ % val
        s = Scenario('demo', expression)
        res = s.execute({})
        self.assertEqual(res, {'res': val, 'rstate': 'Success'})
