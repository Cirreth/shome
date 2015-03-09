__author__ = 'cirreth'

from threading import active_count
#from core.actproctree.AbstractNode_OLD import AbstractNode
import logging

class SchedulerNode(AbstractNode):
    """Controls scheduler module"""

    """Executive plugin name"""
    _task = None
    """Unique identifier will be sended to executive plugin"""
    _action = None
    """New scheme for task"""
    _newscheme = None

    def __init__(self, process_tag, structure):
        super().__init__(process_tag, structure)
        logging.debug('Scheduler node constructing...')

    def __build__(self):
        self._task = self._structure['task'][1:-1]
        self._action = self._structure['action'][1:-1]
        if self._action == 'setscheme':
            if 'scheme' in self._structure:
                self._newscheme = self._structure['scheme'][1:-1]
            else:
                raise Exception('New scheme was not presented')
        self._next = self.create_direction('next')
        self._parallel = self.create_direction('parallel')
        self._exceptional = self.create_direction('exceptional')

    def execute(self, values={}):
        def execute_wrapper(plugin, ref, val, ret):
            ac = active_count()
            self._action_processor.active_threads = ac
            logging.info('Threads alive: ' + str(ac))
            try:
                res = AbstractNode.performer.call(plugin, ref, val)
            except Exception as e:
                res = str(e)
            ret.put(res)
            logging.debug('Thread with ref ( '+ref+' ) evaluation result: '+str(ret.queue[0]))
        logging.debug('Executed SchedulerNode with (task '+self._task+', action '+self._action+', newscheme '+str(self._newscheme)+' )')
        #Current NODE
        self.config_scheduler(self._task, self._action, self._newscheme)
        #
        #CALL PARALLEL
        self.execute_direction(self._parallel, values)
        #
        logging.debug('All parallel nodes of process '+self._process_tag+' completed')
        #CALL NEXT
        self.execute_direction(self._next, values)
        logging.debug('All ways of SchedulerNode '+self._task + ' ' + self._action +' completed')

    def config_scheduler(self, task, action, scheme):
        if action == 'start':
            return self._scheduler.start(task)
        elif action == 'stop':
            return self._scheduler.stop(task)
        elif action == 'setscheme':
            if scheme:
                return self._scheduler.setscheme(task, scheme)
        else:
            raise Exception('Unknown action '+action)

    def get_node_required_keys(self):
        return ['task', 'action']
