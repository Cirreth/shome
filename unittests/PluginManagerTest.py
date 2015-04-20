import os
import logging
import unittest
from core.Database import Database
from core.PluginManager import PluginManager
from core.entities.Plugin import Plugin


class PluginManagerTest(unittest.TestCase):

    cfg = Database()
    Plugin._config = cfg
    cfg.create_database()

    def test_loading(self):
        try:
            p0 = Plugin('mock0', 'mock')
            p0.save()
            p1 = Plugin('mock1', 'mock')
            p1.save()
            pm = PluginManager()
            self.assertEqual(pm.list_all().sort(), ['mock0', 'mock1'].sort())
        finally:
            p0.delete()
            p1.delete()

    def test_call(self):
        try:
            p0 = Plugin('mock0', 'mock')
            p0.save()
            pm = PluginManager()
            self.assertEqual(pm.call_plugin('mock0', 'test'), 'test')
        finally:
            p0.delete()