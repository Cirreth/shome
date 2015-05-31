import tornado
from tornado.web import RequestHandler, HTTPError


class ScenariosListAllHandler(RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self):
        self.finish({"scenarios":  [scenario.dict() for name, scenario in self._ws.action_processor.list_all()]})


class ScenariosHandler(tornado.web.RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self, name):
        scenario = self._ws.action_processor.get_scenario(name)
        if scenario:
            self.finish(scenario.dict())
        else:
            raise HTTPError(404, "Scenario not found")

    def put(self, name):
        data = tornado.escape.json_decode(self.request.body)
        description = data['description'] if 'description' in data else None
        expression = data['expression'] if 'expression' in data else None
        runoninit = data['runoninit'] if 'runoninit' in data else None
        published = data['published'] if 'published' in data else None
        """if description:
            raise NotImplementedError('Description update not supported yet')
        if newtag:
            raise NotImplementedError('Process renaming not supported yet')
        """
        try:
            self._ws.action_processor.update_scenario(
                name=name,
                expression=expression,
                description=description,
                published=published,
                runoninit=runoninit
            )
            self.finish({"result": "success"})
        except Exception as e:
            raise HTTPError(500, str(e))

    def post(self, tag):
        data = tornado.escape.json_decode(self.request.body)
        description = data['description'] if 'description' in data else None
        expression = data['expression'] if 'expression' in data else None
        if expression:
            self._ws.action_processor.add_scenario(tag, expression, save=True)
            self.finish({"result": "success"})

    def delete(self, name):
        self._ws.action_processor.delete_scenario(name)
        self.finish({"result": "success"})