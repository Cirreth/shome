import os
import logging
import unittest
from core.Config import Config
from core.Performer import Performer
from core.entities.Plugin import Plugin

class PerformerTest(unittest.TestCase):

    class Context:

        performer = None
        config = None

        def __init__(self):
            os.remove('config.db')
            self.config = Config()
            self.performer = Performer()
            self.performer.init(self)
            self.config.create_database()
            logging.info('Context initialized')

    context = Context()

    def test_plugin_crud(self):
        pl0 = Plugin('mock0', 'mock')
        pl0.save()
        pl1 = Plugin.get('mock0')
        self.assertEqual(pl0, pl1)
        pl0.set_parameter('port', 4300)
        pl0.save()
        pl2 = Plugin.get('mock0')
        self.assertEqual(pl2._params, '{"port": 4300}')
        pl0.delete()
        pl3 = Plugin.get('mock0')
        self.assertEqual(pl3, None)
        pl0 = Plugin('mock11', 'mock')
        pl1 = Plugin('mock12', 'mock')
        pl0.save()
        pl1.save()
        r = Plugin.get_all()
        self.assertEqual(len(Plugin.get_all()), 2)
        for p in r:
            p.delete()

    def test_plugin_loading(self):
        pl = Plugin('mock', 'mock')
        pl.save()
        self.context.performer.reload_plugins()
        self.assertEqual(self.context.performer._plugins['mock'].instname, pl.instname)
        pl.delete()