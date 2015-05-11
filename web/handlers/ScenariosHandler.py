import tornado
from tornado.web import RequestHandler

class ScenariosListAllHandler(RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self):
        self.finish({"scenarios": self._ws.action_processor.list_all()})


class ScenariosHandler(tornado.web.RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self, name):
        self.finish(self._ws.action_processor.get_scenario(name))

    def put(self, tag):
        data = tornado.escape.json_decode(self.request.body)
        newtag = data['tag'] if 'tag' in data else None
        description = data['description'] if 'description' in data else None
        expression = data['expression'] if 'expression' in data else None
        runoninit = data['runoninit'] if 'runoninit' in data else False
        published = data['published'] if 'published' in data else False
        """if description:
            raise NotImplementedError('Description update not supported yet')
        if newtag:
            raise NotImplementedError('Process renaming not supported yet')
        """
        try:
            if expression:
                self.write(self._ws.action_processor.update_process(
                    tag, expression, description, published, runoninit))
        except Exception as e:
            self.write(e)


    def post(self, tag):
        data = tornado.escape.json_decode(self.request.body)
        description = data['description'] if 'description' in data else None
        expression = data['expression'] if 'expression' in data else None
        if expression:
            self.write(self._ws._action_processor.create_process(tag, expression, writedb=True))

    def delete(self, tag):
        self._ws._action_processor.delete_process(tag)
        self.write('Success')
