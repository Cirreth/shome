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
        task_type = data['type'] if 'type' in data else None
        scheme = data['scheme'] if 'scheme' in data else None
        description = data['description'] if 'description' in data else None
        enabled = data['enabled'] if 'enabled' in data else None
        scenario = data['scenario'] if 'scenario' in data else None
        logging.debug('SchedulerTaskHandler post: '+name+' // {process: '+str(scenario)+', enabled:'+ \
            str(enabled)+', type: '+str(task_type)+', scheme: '+str(scheme)+', description: '+str(description))
        self._ws.scheduler.create_task(scenario=scenario, name=name, scheme=scheme, enabled=enabled,
                                       task_type=task_type, description=description)
        self.finish({"result": "success"})

    def put(self, name):
        data = tornado.escape.json_decode(self.request.body)
        task_type = data['type'] if 'type' in data else None
        scheme = data['scheme'] if 'scheme' in data else None
        description = data['description'] if 'description' in data else None
        enabled = data['enabled'] if 'enabled' in data else None
        scenario = data['scenario'] if 'scenario' in data else None
        logging.debug('SchedulerTaskHandler put: '+name+' // {scenario: '+str(scenario)+', enabled:'+ \
            str(enabled)+', type: '+str(task_type)+', scheme: '+str(scheme)+', description: '+str(description))
        self._ws.scheduler.change_task(name=name, task_type=task_type, scheme=scheme, description=description,
                                                 enabled=enabled, scenario=scenario)
        self.finish({"result": "success"})

    def delete(self, name):
        logging.debug('SchedulerTaskHandler delete: '+name)
        try:
            self._ws.scheduler.delete_task(name)
            self.finish({"result": "success"})
        except Exception as e:
            raise HTTPError(500, str(e))