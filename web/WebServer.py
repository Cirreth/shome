import json
import logging
import re
import uuid

__author__ = 'cirreth'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

from tornado.options import define, options


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        return self.render("views/main.tpl")

class SchedulerAllTasksHandler(tornado.web.RequestHandler):
    """Serves /admin/scheduler/alltasks. Return tasklist"""

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self):
        self.write(json.dumps(self._ws._scheduler.list_all()).encode())

class SchedulerTaskHandler(tornado.web.RequestHandler):
    """Single task REST service"""
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self, title):
        self.write(json.dumps(self._ws._scheduler.get_by_title(title)))

    def post(self, title):
        logging.debug('SchedulerTaskHandler post: '+title)

    def put(self, title):
        logging.debug('SchedulerTaskHandler put: '+title)

    def delete(self, title):
        logging.debug('SchedulerTaskHandler delete: '+title)


class CommandHandler(tornado.web.RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def post(self):
        try:
            cmd = self.get_argument('command')
            res = self._ws.process_message(cmd)
            if res:
                if isinstance(res, str):
                    self.write(res)
                else:
                    self.write(json.dumps(res))
            else:
                self.write('Accepted')

        except Exception as e:
            return self.write(str(e))

class JQueryHandler(tornado.web.RequestHandler):

    def get(self):
        return self.render("js/jquery-2.1.1.min.js")

class WebServer():

    _action_processor = None
    _scheduler = None

    define("port", default=8082, type=int)

    def __init__(self, context):
        self._action_processor = context.action_processor
        self._scheduler = context.scheduler
        self.init_ws()

    def init_ws(self):
        tornado.options.parse_command_line()
        logging.getLogger().setLevel(logging.DEBUG)
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "admin_path": os.path.join(os.path.dirname(__file__), "admin"),
        }
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/command", CommandHandler, {'ws': self}),
            (r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
            (r"/admin/scheduler/alltasks", SchedulerAllTasksHandler, {'ws': self}),
            (r"/admin/scheduler/task/(.+)", SchedulerTaskHandler, {'ws': self}),
            (r"/admin/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['admin_path'])),
        ], debug=True, **settings)
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

    def process_message(self, message):
        """
        Command line handler
        """
        logging.debug('Message recieved: body ( '+message+' )')
        if message.startswith('process'):
            logging.debug('Input string interpreted as request to process reconfiguring ( '+message)
            msg = re.search('^process create (.+?)\\s*:\\s*((.*\\n?)+)', message, re.MULTILINE)
            if msg and msg.group(0):
                logging.debug('Input parsed as: create process with name ( '+msg.group(1)+' ) and definition ( '+msg.group(3))
                return self._action_processor.create_process(msg.group(1), msg.group(2), writedb=True)
            msg = re.search('^process update (.+?)\\s*:\\s*((.*\\n?)+)', message, re.MULTILINE)
            if msg and msg.group(0):
                logging.debug('Input parsed as: update process with name ( '+msg.group(1)+' ) and definition ( '+msg.group(2))
                return self._action_processor.update_process(msg.group(1), msg.group(2))
            msg = re.search('^process list$', message)
            logging.debug('process list requested')
            if msg and msg.group(0):
                return self._action_processor.list_all()
            msg = re.search('^process get (.*)', message)
            if msg and msg.group(0):
                return '<b>'+msg.group(1)+' definition:</b><br/>'+self._action_processor.get_process(msg.group(1))
            msg = re.search('^process delete (.*)', message)
            if msg and msg.group(0):
                procname = msg.group(1)
                try:
                    schd = self._scheduler.delete_like(procname)
                    acpd = self._action_processor.delete_process(procname)
                except Exception as e:
                    return 'Operation (delete '+procname+') failed: '+str(e)
                return '<b>'+procname+' delete command result:</b><br/>Scheduler: '+str(schd)+'<br/>ActionProcessor: '+str(acpd)
        elif message.startswith('schedule'):

            msg = re.search('^schedule create (.+?)\\s*:\\s*((.*\\n?)+)', message, re.MULTILINE)
            if msg and msg.group(0):
                logging.debug('Input parsed as: schedule command ( '+msg.group(1)+' ) with scheme(interval) ( '+msg.group(2)+' )')
                return self._scheduler.create(msg.group(1), msg.group(2), writedb=True)

            msg = re.search('^schedule setscheme (.+?)\\s*:\\s*((.*\\n?)+)', message, re.MULTILINE)
            if msg and msg.group(0):
                logging.debug('Input parsed as: schedule command ( '+msg.group(1)+' ) with scheme(interval) ( '+msg.group(2)+' )')
                return self._scheduler.setscheme(msg.group(1), msg.group(2))

            msg = re.search('^schedule start (.+)', message)
            if msg and msg.group(0):
                logging.debug('Input parsed as: start scheduled command ( '+msg.group(1)+' )')
                return self._scheduler.start(msg.group(1))

            msg = re.search('^schedule stop (.+)', message)
            if msg and msg.group(0):
                logging.debug('Input parsed as: stop scheduled command ( '+msg.group(1)+' )')
                return self._scheduler.stop(msg.group(1))

            msg = re.search('^schedule delete (.+)', message)
            if msg and msg.group(0):
                logging.debug('Input parsed as: delete scheduled command ( '+msg.group(1)+' )')
                return self._scheduler.delete(msg.group(1))
            if message == 'schedule list':
                return self._scheduler.list_all()
        elif message.startswith('system'):
            if message == 'system threads':
                return 'Active threads: '+str(self._action_processor.active_threads)
        elif message.startswith('test'):
            msg = re.search('^test ((.*\\n?)+?\})(:)?((?(2)[.\\n]+))', message, re.MULTILINE)
            if msg and msg.group(0):
                gid = 'chk'+str(uuid.uuid4())
                self._action_processor.create_process(gid, msg.group(1))
                vals = msg.group(3) if msg.group(3) else ''
                res = self._action_processor.process(gid+vals)
                #@TODO move to action processor, create interface
                del self._action_processor._processes[gid]
                return res

        #если ничего не подошло
        logging.debug('Input string interpreted as process tag')
        return self._action_processor.process(message)
