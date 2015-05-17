from core import Scheduler
from core.PluginManager import PluginManager
from web.WebServer import WebServer

__author__ = 'cirreth'
from core.Database import Database
from core.ActionProcessor import ActionProcessor
import logging


class Context:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s',
                            filename='debug.log', filemode='w')
        self.config = Database()
        self.plugin_manager = PluginManager()
        self.action_processor = ActionProcessor()
        self.scheduler = Scheduler(self.action_processor)
        logging.info('Context initialized')

        #start web server
        self.web_server = WebServer(self)
        logging.info('Server started')