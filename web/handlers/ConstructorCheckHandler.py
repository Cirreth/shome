import uuid
import tornado

class ConstructorCheckHandler(tornado.web.RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        expression = data['expression'] if 'expression' in data else None
        parameters = data['parameters'] if 'parameters' in data else None
        if expression:
            gid = 'chk'+str(uuid.uuid4())
            self._ws.action_processor.add_scenario(gid, expression)
            res = self._ws.action_processor.execute(gid, {})
            self._ws.action_processor.delete_scenario(gid)
            if res:
                self.finish(res)
        else:
            raise tornado.HTTPError(405, "Expression is not defined")