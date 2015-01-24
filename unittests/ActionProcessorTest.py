import time
from core.Config import Config
from core.ActionProcessor import ActionProcessor
from core.Scheduler import Scheduler
from core.Performer import Performer
import os
import logging
import unittest

class ActionProcessorTest(unittest.TestCase):

    class Context:

        action_processor = None
        scheduler = None
        performer = None
        socket_server = None
        config = None

        def __init__(self):
            os.chdir("../")
            logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='unittests/debug.log', filemode='w')
            self.config = Config()
            self.action_processor = ActionProcessor()
            self.scheduler = Scheduler()
            self.performer = Performer()
            self.action_processor.init(self)
            self.scheduler.init(self)
            self.performer.init(self)
            logging.info('Context initialized')

    context = Context()
    delproc = context.action_processor.delete_process
    createproc = context.action_processor.create_process
    process = context.action_processor.execute

    def test_actionprocessor_create_execute(self):
        """Create process, execute and delete it"""
        self.createproc('runmock', """{
                                          "type": "RequestNode",
                                          "plugin": "mock",
                                          "reference": "test ActionProcessor create execute delete",
                                          "retvar":"x"
                                        }""")
        self.assertEqual(self.process('runmock'), {'x': 'test ActionProcessor create execute delete'})