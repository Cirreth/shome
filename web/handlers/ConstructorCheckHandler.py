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
            self._ws._action_processor.create_process(gid, expression)
            parameters = '{'+parameters+'}' if parameters else ''
            res = self._ws._action_processor.execute(gid+parameters)
            self._ws._action_processor.delete_process(gid)
            if (res):
                self.write(res)
        else:
            raise tornado.HTTPError(422, "Expression is not defined")