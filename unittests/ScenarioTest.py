import os
import logging
import unittest
import time
from core.actproctree.NodeBuilder import NodeBuilder
from core.entities.Scenario import Scenario

logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')


class ScenarioTest(unittest.TestCase):

    scenario_1 = """
    [
        {
          "id": "Start",
          "type": "StartNode",
          "next": [
            "rn490",
            "rn361"
          ],
          "parallel": [],
          "dimension": {
            "width": 90,
            "height": 32
          },
          "active": false
        },
        {
          "id": "rn490",
          "type": "RequestNode",
          "plugin": "mock",
          "reference": "change me",
          "position": {
            "left": 267,
            "top": 144
          },
          "next": [],
          "parallel": [
            "rn245",
            "rn35"
          ],
          "exceptional": [],
          "dimension": {
            "width": 180,
            "height": 65
          },
          "active": false
        },
        {
          "id": "rn245",
          "type": "DelayNode",
          "delay": 0,
          "position": {
            "left": 529,
            "top": 258
          },
          "next": [],
          "parallel": [],
          "exceptional": [],
          "dimension": {
            "width": 60,
            "height": 60
          },
          "active": false
        },
        {
          "id": "rn35",
          "type": "RequestNode",
          "plugin": "mock",
          "reference": "change me",
          "position": {
            "left": 401,
            "top": 373
          },
          "next": [],
          "parallel": [],
          "exceptional": [],
          "dimension": {
            "width": 180,
            "height": 65
          }
        },
        {
          "id": "rn361",
          "type": "RequestNode",
          "plugin": "mock",
          "reference": "change me",
          "retvar": "res",
          "position": {
            "left": 593,
            "top": 152
          },
          "next": [],
          "parallel": [],
          "exceptional": [],
          "dimension": {
            "width": 180,
            "height": 65
          }
        }
    ]
    """

    scenario_2 = """
    [
        {
          "id": "Start",
          "type": "StartNode",
          "next": [
            "rn144",
            "rn148"
          ],
          "parallel": [],
          "dimension": {
            "width": 90,
            "height": 32
          },
          "active": false
        }, {
          "id": "rn144",
          "type": "RequestNode",
          "plugin": "mock",
          "reference": "right",
          "position": {
            "left": 360,
            "top": 175
          },
          "next": [],
          "parallel": [],
          "exceptional": [],
          "dimension": {
            "width": 180,
            "height": 65
          },
          "active": false,
          "retvar": "b"
        }, {
          "id": "rn148",
          "type": "RequestNode",
          "plugin": "mock",
          "reference": "left",
          "position": {
            "left": 152,
            "top": 175
          },
          "next": [],
          "parallel": [],
          "exceptional": [],
          "dimension": {
            "width": 180,
            "height": 65
          },
          "active": false,
          "retvar": "a"
        }
    ]
    """

    def test_scenario_1(self):
        sc1 = Scenario('scenario_1', self.scenario_1)
        sc1.construct()
        sc1.execute({})

    def test_scenario_2(self):
        sc2 = Scenario('scenario_2', self.scenario_2)
        sc2.construct()
        self.assertEqual(sc2.execute({}), {'a': 'left', 'b': 'right'})