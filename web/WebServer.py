import os
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from .handlers import *


class WebServer():

    define("port", default=8082, type=int)

    def __init__(self, context):
        self.context = context
        self.action_processor = context.action_processor
        self.plugin_manager = context.plugin_manager
        self.scheduler = context.scheduler
        self.init_ws()

    def init_ws(self):
        tornado.options.parse_command_line()
        logging.getLogger().setLevel(logging.DEBUG)
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "resources"),
            "app_path": os.path.join(os.path.dirname(__file__), "app"),
            "admin_path": os.path.join(os.path.dirname(__file__), "admin"),
        }
        application = tornado.web.Application([
            (r"/resources/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
            (r"/app/(.*)", tornado.web.StaticFileHandler, dict(path=settings['app_path'])),
            (r"/admin/scheduler/tasks", SchedulerAllTasksHandler, {'ws': self}),
            (r"/admin/scheduler/task/(.+)", SchedulerTaskHandler, {'ws': self}),
            (r"/admin/scenarios/", ScenariosListAllHandler, {'ws': self}),
            (r"/admin/scenarios/(.+)", ScenariosHandler, {'ws': self}),
            (r"/admin/constructor/check", ConstructorCheckHandler, {'ws': self}),
            (r"/admin/plugins", PluginManagementHandler, {'ws': self}),
            (r"/admin/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['admin_path'])),
            (r"/(.*)", MainHandler),
        ], debug=True, **settings)
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()