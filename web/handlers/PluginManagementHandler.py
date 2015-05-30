import json
from tornado.web import RequestHandler


class PluginManagementHandler(RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self):
        self.finish({"plugins": self._ws.context.plugin_manager.list_all()})
