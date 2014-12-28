import queue

__author__ = 'cirreth'
import logging
import threading

#@TODO Needs full refactoring. Reason: pk changed to 'title'
class Scheduler:

    _action_processor = None
    _configuration = None
    _frequent = {}
    _scheduled = {}

    class Task:

        _action_processor = None
        procname = None
        stopped = True
        title = None
        description = None

        def __init__(self, ap, procname, title, description):
            self._action_processor = ap
            self.procname = procname
            self.description = description
            self.title = title

    class FrequentTask(Task):

        interval = None
        _timer = None

        def __init__(self, ap, procname, title, interval, description):
            super().__init__(ap, procname, title, description)
            self.interval = interval
            self._queue = queue.Queue()

        def start(self):
            logging.debug(self.procname+' started')
            self.stopped = False
            def tick():
                if self.stopped:
                    return
                self._action_processor.process(self.procname)
                t = threading.Timer(self.interval, tick)
                t.start()
                return t
            self._timer = tick()

        def stop(self):
            logging.debug(self.procname+' stopping...')
            if not self.stopped:
                self.stopped = True
                self._timer.cancel()

        def dict_repr(self):
            return {
                'title': self.title,
                'description': self.description,
                'process': self.procname,
                'type': 'interval',
                'scheme': self.interval,
                'isrunned': not self.stopped
            }

    class ScheduledTask(Task):
        """NOT IMPLEMENTED"""

        """Cron-like time format"""
        expression = None

        def __init__(self):
            raise NotImplementedError

        def dict_repr(self):
            return {
                'process': self._procname,
                'schema': self.expression,
                'isrunned': self.stopped
            }


    def __init__(self):
        pass

    def init(self, context):
        logging.debug("Scheduler initialization")
        self._action_processor = context.action_processor
        self._configuration = context.config

    def create(self, procname, title, timeschema, isrunned=False, description='', writedb=False):
        if self.get_by_title(title):
            return 'Task with title '+title+' already scheduled'
        try:
            interval = float(timeschema)
            self._frequent[procname] = Scheduler.FrequentTask(self._action_processor, procname, title, interval, description)
            if isrunned:
                self._frequent[procname].start()
            if description:
                self._frequent[procname].description = description
            msg = ''
            if writedb:
                try:
                    self._configuration.add_task(procname, title, timeschema, isrunned, description)
                except Exception as e:
                   msg = ', but database does not updated. Reason:'+str(e)
            return 'Succesefuly created'+msg
        except ValueError:
            # not interval => scheduled
            raise NotImplementedError

    def setscheme(self, procname, scheme):
        procname = procname.strip()
        if self.get_by_procname(procname):
            try:
                wasrunned = False
                if self.get_by_procname(procname).isrunned:
                    wasrunned = True
                    self.stop(procname)
                interval = float(scheme)
                self._frequent[procname].interval = interval
                if wasrunned:
                    self.start(procname)
                msg = ''
                try:
                    self._configuration.update_task(procname, scheme, wasrunned)
                except Exception as ex:
                    msg = ', but database not updated'
                return 'Scheme for '+procname+' successfully changed on '+scheme + msg
            except ValueError:
                return 'Not implemented for scheduled (not frequent) processes'

    def start(self, title):
        task = self.get_by_title(title)
        if task:
            if not task.stopped:
                raise Exception('Task '+title+' already running')
            task.start()
            msg = ''
            try:
                #@TODO replace task.interval on task.get_schema
                self._configuration.update_task(task.procname, title, task.interval, True)
            except Exception as e:
                msg = ', but not saved in database: '+str(e)
            return title+' in scheduler is started'+msg

    def stop(self, title):
        task = self.get_by_title(title)
        if task:
            task.stop()
            self._configuration.update_task(task.procname, title, task.interval, False)

    def get_by_procname(self, procname):
        if procname in self._frequent:
            return self._frequent[procname]
        elif procname in self._scheduled:
            return self._scheduled[procname]
        else:
            return None

    def get_by_title(self, title):
        for procname in self._frequent:
            if self._frequent[procname].title == title:
                return self._frequent[procname]
        for procname in self._scheduled:
            if self._scheduled[procname].title == title:
                return self._scheduled[procname]
        return None


    def find(self, procname):
        """Find all tasks whose name contains procname"""
        res = []
        for k in list(self._frequent.keys()) + list(self._scheduled.keys()):
            if procname in k:
                res += k
        return res

    def delete_like(self, procname):
        """
            Delete all processes whose name contains procname
        """
        prcs = self.find(procname)
        res = {}
        for k in prcs:
            res[k] = self.delete(k)
        return res

    def delete(self, title):
        logging.debug('trying to delete task with title '+title+' from scheduler')
        try:
            task = self.get_by_title(title)
            task.stop()
            for procname in self._frequent:
                if self._frequent[procname].title == title:
                    del self._frequent[procname]
                    break
            for procname in self._scheduled:
                if self._scheduled[procname].title == title:
                    del self._scheduled[procname]
                    break
            try:
                self._configuration.delete_task(title)
            except Exception as es:
                return 'Deleted from scheduler, but not from configuration. '+str(es)
        except Exception as e:
            return str(e)

    def list_all(self):
        return [self._frequent[t].dict_repr() for t in self._frequent] + [self._scheduled[t].dict_repr() for t in self._scheduled]