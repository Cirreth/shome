import logging
import unittest
from core.Database import Database
from core.PluginManager import PluginManager
from core.entities.Scenario import Scenario

logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')
cfg = Database()
cfg.create_database()
#mp = Plugin('mock', 'mock').save()
p = PluginManager()


class ScenarioTest(unittest.TestCase):

    scenario_1 = """

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

    scenario_3_conditional = """
    [
        {
          "id": "Start",
          "type": "StartNode",
          "next": [
            "cn144"
          ],
          "parallel": [],
          "dimension": {
            "width": 90,
            "height": 32
          },
          "active": false
        }, {
          "id": "cn144",
          "type": "ConditionalNode",
          "expression": "1 === 1",
          "position": {
            "left": 360,
            "top": 175
          },
          "yes": ["rn148"],
          "no": [],
          "dimension": {
            "width": 180,
            "height": 65
          }
        },
        {
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
        pass
        #sc1 = Scenario('scenario_1', self.scenario_1)
        #sc1.construct()
        #sc1.execute({})

    def test_scenario_2(self):
        sc2 = Scenario('scenario_2', self.scenario_2)
        sc2.construct()
        self.assertEqual(sc2.execute({}), {'a': 'left', 'b': 'right'})

    def test_scenario_3(self):
        sc1 = Scenario('scenario_1', self.scenario_3_conditional)
        sc1.construct()
        self.assertEqual(sc1.execute({}), {'a': 'left'})
        self.scenario_3_conditional = self.scenario_3_conditional.replace('1 === 1', 'false')
        sc2 = Scenario('scenario_2', self.scenario_3_conditional)
        sc2.construct()
        self.assertEqual(sc2.execute({}), {})