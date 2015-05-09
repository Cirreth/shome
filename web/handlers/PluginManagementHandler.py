import json
from tornado.web import RequestHandler


class PluginManagementHandler(RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self, path):
        if path == 'active':
            self.write(json.dumps(self._ws._performer.list_loaded_plugins()))
        elif path == 'all':
            self.write(json.dumps(self._ws._performer.list_all_plugins()))
