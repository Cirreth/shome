from core.Configuration import Configuration
from core.ActionProcessor import ActionProcessor
from core.Scheduler import Scheduler
from core.Performer import Performer
import os
import logging
import unittest

class MyTestCase(unittest.TestCase):

    class Context:

        action_processor = None
        scheduler = None
        performer = None
        socket_server = None
        config = None

        def __init__(self):
            os.chdir("../")
            logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='unittests/debug.log', filemode='w')
            self.config = Configuration()
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
    process = context.action_processor.process

    def test_actionprocessor_create_execute_delete(self):
        """Create process, execute and delete it"""
        self.createproc('runmock', """{
                                          "type": "RequestNode",
                                          "plugin": "mock",
                                          "reference": "test ActionProcessor create execute delete",
                                          "retvar":"x"
                                        }""")
        self.assertEqual(self.process('runmock'), {'x': 'test ActionProcessor create execute delete'})
        self.delproc('runmock')
        self.assertEqual('runmock' in self.context.action_processor._processes, False)

    def test_schedulernode_create_start_stop(self):
        """
            1. Create SchedulerNode
            2. Start process
            3. Stop process
        """
        self.createproc('sch-css', """{"type": "RequestNode",
                            "plugin": "mock", "reference": "test SchedulerNode create start stop", "retvar": "x"}""")
        self.context.scheduler.create('sch-css', 1)
        self.createproc('start-sch-css', """{"type":"SchedulerNode","task":"sch-css","action":"start"}""")
        self.createproc('stop-sch-css', """{"type":"SchedulerNode","task":"sch-css","action":"stop"}""")
        self.assertEqual(self.context.scheduler._frequent['sch-css'].stopped, True)
        self.process('start-sch-css')
        self.assertEqual(self.context.scheduler._frequent['sch-css'].stopped, False)
        self.process('stop-sch-css')
        self.assertEqual(self.context.scheduler._frequent['sch-css'].stopped, True)
        self.delproc('start-sch-css')
        self.delproc('stop-sch-css')
        self.delproc('sch-css')

    def test_executenode_create_execute(self):
        """Start another process by ExecuteNode. Child process variables ignored"""
        self.createproc('execnode-ce', """{"type": "RequestNode",
                            "plugin": "mock", "reference": "test ExecuteNode create execute", "retvar": "x"}""")
        self.assertEqual(self.process('execnode-ce'), {'x': 'test ExecuteNode create execute'})
        self.createproc('exec-execnode-ce', '{"type": "ExecuteNode", "name": "execnode-ce"}')
        self.assertEqual(self.process('exec-execnode-ce'), None)
        self.delproc('exec-execnode-ce')
        self.delproc('execnode-ce')

    def test_executenode_create_execute_with_mergevars(self):
        """Start another process by ExecuteNode. Child process variables are pushed in parent process"""
        self.createproc('execnode-mergevars', """{"type": "RequestNode",
                            "plugin": "mock", "reference": "test ExecuteNode create execute with variables merging", "retvar": "x"}""")
        self.assertEqual(self.process('execnode-mergevars'), {'x': 'test ExecuteNode create execute with variables merging'})
        self.createproc('exec-execnode-mergevars', '{"type": "ExecuteNode", "name": "execnode-mergevars", "mergevars":true}')
        self.assertEqual(self.process('exec-execnode-mergevars'), {'x': 'test ExecuteNode create execute with variables merging'})
        self.delproc('exec-execnode-mergevars')
        self.delproc('execnode-mergevars')
