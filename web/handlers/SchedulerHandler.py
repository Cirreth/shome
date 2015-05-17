import logging
import tornado
from tornado.web import RequestHandler, HTTPError


class SchedulerAllTasksHandler(RequestHandler):

    #web server instance
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self):
        self.finish({"tasks": self._ws.scheduler.list_all()})


class SchedulerTaskHandler(RequestHandler):
    """Single task REST service"""
    _ws = None

    def initialize(self, ws):
        self._ws = ws

    def get(self, name):
        self.finish(self._ws.scheduler.get(name))

    def post(self, name):
        data = tornado.escape.json_decode(self.request.body)
        tasktype = data['type'] if 'type' in data else None
        scheme = data['scheme'] if 'scheme' in data else None
        description = data['description'] if 'description' in data else None
        enabled = data['enabled'] if 'enabled' in data else None
        process = data['process'] if 'process' in data else None
        logging.debug('SchedulerTaskHandler post: '+name+' // {process: '+str(process)+', enabled:'+ \
            str(enabled)+', type: '+str(tasktype)+', scheme: '+str(scheme)+', description: '+str(description))
        self.finish({"result": "success"})
        self._ws.scheduler.create(process, name, scheme, enabled, description, save=True)

    def put(self, name):
        data = tornado.escape.json_decode(self.request.body)
        tasktype = data['type'] if 'type' in data else None
        scheme = data['scheme'] if 'scheme' in data else None
        description = data['description'] if 'description' in data else None
        enabled = data['enabled'] if 'enabled' in data else None
        process = data['process'] if 'process' in data else None
        logging.debug('SchedulerTaskHandler put: '+name+' // {process: '+str(process)+', enabled:'+ \
            str(enabled)+', type: '+str(tasktype)+', scheme: '+str(scheme)+', description: '+str(description))
        if enabled is not None:
            if enabled:
                self._ws.scheduler.start_task(name)
            else:
                self._ws.scheduler.stop_task(name)

    def delete(self, name):
        logging.debug('SchedulerTaskHandler delete: '+name)
        try:
            self._ws.scheduler.delete(name)
            self.finish()
        except Exception as e:
            raise HTTPError(500, str(e))