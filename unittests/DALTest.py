import os
import unittest
from core.entities.Plugin import Plugin
from core.entities.Scenario import Scenario
from core.Database import Database
from core.entities.Task import Task


class MyTestCase(unittest.TestCase):
    os.remove('config.db')
    conf = Database()
    conf.create_database()

    def test_plugin_CRUD(self):
        pl = Plugin(instname='test0',
                    name='plugin0')
        pl.save()
        pll = Plugin.get('test0')
        self.assertEqual(pl, pll)
        pl.set_param('p0', 3)
        pl.save()
        pll = Plugin.get('test0')
        self.assertEqual(pll.get_params(), {'p0': 3})
        pl.delete()
        pll = Plugin.get('test0')
        self.assertEqual(pll, None)

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

    def test_task_CRUD(self):
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
        tsk = Task(name='test0',
                   scenario='test_sc_0',
                   task_type='interval',
                   scheme='10',
                   enabled=True
        )
        tsk.save()
        tskl = Task.get('test0')
        self.assertEqual(tsk, tskl)
        tsk.description = "demo descr"
        tsk.save()
        tskl = Task.get('test0')
        self.assertEqual(tskl.description, "demo descr")
        tsk.delete()
        sc.delete()
        tskl = Task.get('test0')
        self.assertEqual(tskl, None)