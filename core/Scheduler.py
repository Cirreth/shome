import queue

__author__ = 'cirreth'
import logging
import threading

class Scheduler:

    _action_processor = None
    _configuration = None
    _frequent = {}
    _scheduled = {}

    class FrequentTask:

        _action_processor = None
        _procname = None
        interval = 0
        _timer = None
        """Set True value when you need to stop task"""
        stopped = True

        def __init__(self, ap, procname, interval):
            self._action_processor = ap
            self._procname = procname
            self.interval = interval
            self._queue = queue.Queue()

        def start(self):
            logging.debug(self._procname+' started')
            self.stopped = False
            def tick():
                if self.stopped:
                    return
                self._action_processor.process(self._procname)
                t = threading.Timer(self.interval, tick)
                t.start()
                return t
            self._timer = tick()

        def stop(self):
            logging.debug(self._procname+' stopped')
            self.stopped = True
            self._timer.cancel()

        def dict_repr(self):
            return {
                'name': self._procname,
                'scheme': self.interval,
                'isrunned': not self.stopped
            }

    class ScheduledTask:

        _procname = None
        """Cron-like time format"""
        expression = None
        isrunned = False

        def dict_repr(self):
            return {
                'name': self._procname,
                'scheme': self.expression,
                'isrunned': self.stopped
            }


    def __init__(self):
        pass

    def init(self, context):
        logging.debug("Scheduler initialization")
        self._action_processor = context.action_processor
        self._configuration = context.config

    def create(self, procname, timescheme, writedb=False):
        if self.get(procname):
            return 'Process with name '+procname+' already scheduled with scheme ' \
            + str(self._frequent[procname].interval) if procname in self._frequent else self._scheduled[procname].expression
        try:
            interval = float(timescheme)
            self._frequent[procname] = Scheduler.FrequentTask(self._action_processor, procname, interval)
            msg = ''
            if writedb:
                try:
                    self._configuration.add_task(procname, timescheme, False)
                except Exception as e:
                   msg = ', but database does not updated. Reason:'+str(e)
            return 'Succesefuly created'+msg
        except ValueError:
            # not interval => scheduled
            raise NotImplementedError

    def setscheme(self, procname, timescheme):
        procname = procname.strip()
        if self.get(procname):
            try:
                wasrunned = False
                if self.get(procname).isrunned:
                    wasrunned = True
                    self.stop(procname)
                interval = float(timescheme)
                self._frequent[procname].interval = interval
                if wasrunned:
                    self.start(procname)
                msg = ''
                try:
                    self._configuration.update_task(procname, timescheme, wasrunned)
                except Exception as ex:
                    msg = ', but database not updated'
                return 'Scheme for '+procname+' successfully changed on '+timescheme + msg
            except ValueError:
                return 'Not implemented for scheduled (not frequent) processes'

    def start(self, procname):
        if procname in self._frequent:
            if not self._frequent[procname].stopped:
                return 'Task with this name already started'
            self._frequent[procname].start()
            msg = ''
            try:
                self._configuration.update_task(procname, self.get(procname).interval, True)
            except Exception as e:
                msg = ', but not saved in database: '+str(e)
            return procname+' in scheduler is started'+msg
        elif procname in self._scheduled:
            raise NotImplementedError

    def stop(self, procname):
        if procname in self._frequent:
            self._frequent[procname].stop()
            msg = ''
            try:
                self._configuration.update_task(procname, self.get(procname).interval, False)
            except Exception as e:
                msg = ', but not saved in database: '+str(e)
            return procname+' in scheduler is stopped'+msg
        elif procname in self._scheduled:
            raise NotImplementedError

    def get(self, procname):
        if procname in self._frequent:
            return self._frequent[procname]
        elif procname in self._scheduled:
            return self._scheduled[procname]
        else:
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

    def delete(self, procname):
        logging.debug('trying to delete process with name '+procname+' from scheduler')
        try:
            if procname in self._frequent:
                self.stop(procname)
                del(self._frequent[procname])
            elif procname in self._scheduled:
                self.stop(procname)
                del(self._scheduled[procname])
            else:
                return procname + ' not found'
            try:
                self._configuration.delete_task(procname)
            except Exception as es:
                return 'Deleted from scheduler, but not from configuration. '+str(es)
            return 'success'
        except Exception as e:
            return str(e)

    def list_all(self):
        return [self._frequent[t].dict_repr() for t in self._frequent] + [self._scheduled[t].dict_repr() for t in self._scheduled]