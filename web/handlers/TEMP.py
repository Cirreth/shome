__author__ = 'Кирилл'


class SchedulerAllTasksHandler(tornado.web.RequestHandler):

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
        data = tornado.escape.json_decode(self.request.body)
        tasktype = data['type'] if 'type' in data else None
        scheme = data['scheme'] if 'scheme' in data else None
        description = data['description'] if 'description' in data else None
        isrunned = data['isrunned'] if 'isrunned' in data else None
        process = data['process'] if 'process' in data else None
        logging.debug('SchedulerTaskHandler post: '+title+' // {process: '+str(process)+', isrunned:'+ \
            str(isrunned)+', type: '+str(tasktype)+', scheme: '+str(scheme)+', description: '+str(description))
        self.write('Success')
        self._ws._scheduler.create(process, title, scheme, isrunned, description, writedb=True)

    def put(self, title):
        data = tornado.escape.json_decode(self.request.body)
        tasktype = data['type'] if 'type' in data else None
        scheme = data['scheme'] if 'scheme' in data else None
        description = data['description'] if 'description' in data else None
        isrunned = data['isrunned'] if 'isrunned' in data else None
        process = data['process'] if 'process' in data else None
        logging.debug('SchedulerTaskHandler put: '+title+' // {process: '+str(process)+', isrunned:'+ \
            str(isrunned)+', type: '+str(tasktype)+', scheme: '+str(scheme)+', description: '+str(description))
        if isrunned is not None:
            if isrunned:
                self._ws._scheduler.start(title)
            else:
                self._ws._scheduler.stop(title)

    def delete(self, title):
        logging.debug('SchedulerTaskHandler delete: '+title)
        try:
            self._ws._scheduler.delete(title)
            self.write(title + ' successfully deleted')
        except Exception as e:
            return str(e)

class ScenariosHandler(tornado.web.RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self, name):
        self.write(self._ws._action_processor.get_process(name))

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
                self.write(self._ws._action_processor.update_process(
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


class ScenariosListAllHandler(tornado.web.RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self):
        self.write(json.dumps(self._ws._action_processor.list_all()))
