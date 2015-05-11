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