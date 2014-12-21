__author__ = 'cirreth'
from core.Configuration import Configuration
from core.ActionProcessor import ActionProcessor
from core.Scheduler import Scheduler
from core.Performer import Performer
from web.WebServer import WebServer
import logging

class Context:

    action_processor = None
    scheduler = None
    performer = None
    socket_server = None
    config = None

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,  format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s', filename='debug.log', filemode='w')
        self.config = Configuration()
        self.action_processor = ActionProcessor()
        self.scheduler = Scheduler()
        self.performer = Performer()
        self.action_processor.init(self)
        self.scheduler.init(self)
        self.performer.init(self)
        logging.info('Context initialized')



        #load processes

        processes = self.config.get_all_processes()

        for k in processes:
            self.action_processor.create_process(k['name'], k['definition'])

        for k in processes:
            if not k['runoninit'] is None:
                self.action_processor.process(k['name'])

        #load tasks
        for k in self.config.get_all_tasks():
            logging.debug('Loading: '+str((k['process'], k['title'], k['description'], k['scheme'], k['isrunned'])))
            self.scheduler.create(k['process'], k['title'], k['scheme'], k['description'])
            if k['isrunned'] is True:
                self.scheduler.start(k['process'])


        self.web_server = WebServer(self)
