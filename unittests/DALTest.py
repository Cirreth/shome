import os
import logging
import unittest
from core.entities.Scenario import Scenario
from core.Config import Config

class MyTestCase(unittest.TestCase):

    conf = Config()
    conf.create_database()

    def test_scenario_CRUD(self):
        sc = Scenario(name='test0',
                      expression="""
                        {
                            "type":"RequestNode",
                            "plugin":"mock",
                            "reference":"0",
                            "retvar":"x"
                        }
                        """,
                      description='blank')
        sc.save()
        scl = Scenario.get('test0')
        self.assertEqual(sc, scl)
        sc.description = 'Test0 description'
        sc.save()
        scl_descr = Scenario.get('test0').description
        self.assertEqual(sc.description, scl_descr)
        sc.delete()
        scld = Scenario.get('test0')
        self.assertEqual(scld, None)


