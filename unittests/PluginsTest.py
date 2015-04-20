import json
import logging
import unittest
from core.Database import Database
from core.entities.Plugin import Plugin

logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')


class PluginsTest(unittest.TestCase):

    config = Database()
    config.create_database()
    Plugin._config = config

    def test_mock_plugin(self):
        mp = Plugin('mock', 'mock')
        self.assertEqual(mp.call('test'), 'test')

    def test_plugin_listall(self):
        mp = Plugin('mock', 'mock')
        mp.save()
        try:
            self.assertEqual(
                [p.json_repr() for p in Plugin.get_all()],
                [{"enabled": True,
                  "instname": "mock",
                  "params": "{}",
                  "name": "mock",
                  "state": "unknown"}]
            )
        finally:
            mp.delete()