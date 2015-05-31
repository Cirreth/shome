import uuid
import tornado


class ListScenariosHandler(tornado.web.RequestHandler):

    #web server instance

    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self):
        self.finish({"list": [name for name, scenario in self._ws.action_processor.list_all() if scenario.published]})


class ExecuteScenarioHandler(tornado.web.RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        scenario = data['scenario'] if 'scenario' in data else None
        parameters = data['parameters'] if 'parameters' in data else {}
        if scenario:
            res = self._ws.action_processor.execute(scenario, parameters)
            if res:
                self.finish(res)
        else:
            raise tornado.HTTPError(405, "Scenario is not defined")