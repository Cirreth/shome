__author__ = 'cirreth'

import queue
from threading import Thread
from core.actproctree.AbstractNode import AbstractNode
import logging

class ExecuteNode(AbstractNode):
    """Execute another process"""

    """Name of process to be executed"""
    _name = None
    """Add results to root process evaluation result set (actionprocessor.pss_variables[_name]) with replace"""
    _mergevars = False

    def __init__(self, process_tag, structure):
        super().__init__(process_tag, structure)
        logging.debug('Execute node constructing...')

    def __build__(self):
        self._name = self._structure['name'][1:-1]
        if 'mergevars' in self._structure:
            self._mergevars = self._structure['mergevars']
        self._next = self.create_direction('next')
        self._parallel = self.create_direction('parallel')
        self._exceptional = self.create_direction('exceptional')

    def execute(self, values={}):
        logging.debug('Executed ExecuteNode for process with name ( '+self._name+' )')
        #CALL NODE
        ret = queue.Queue()
        uid = 'abcde'
        current_thread = Thread(target=AbstractNode._action_processor.process, args=(self._name,ret,uid))
        current_thread.start()
        #
        #CALL PARALLEL
        self.execute_direction(self._parallel, values)
        #
        logging.debug('current node thread joined to main')
        current_thread.join()
        ret = ret.get()
        logging.debug('From ExecuteNode ('+self._name+' recieved '+str(ret))
        if self._mergevars:
            for k in ret:
                AbstractNode._action_processor.update_proc_var(self._process_tag, k, ret[k])
        logging.debug('All parallel nodes of process '+self._process_tag+' completed')
        #CALL NEXT
        self.execute_direction(self._next, values)
        logging.debug('All ways of ExecuteNode for ('+self._name+') completed')

    def __prepare_value(self, values):
        pvars = self._action_processor.pss_variables
        val = None  #will be used as value argument
        #Use value if setted
        if not self._value is None:
            val = self._value
        #иначе должно быть установлено имя переменной
        elif self._variable:
            key = next(iter(self._variable.keys()))
            #ищем сначала в переданных пользователем параметрах
            if key in values:
                val = values[key]
            elif self._process_tag in pvars and key in pvars[self._process_tag]:
                val = pvars[self._process_tag][key]
            #если там тоже нет, ищем в предустановленных переменных
            elif self._variable[key]:
                val = self._variable[key]
            #если нигде не нашли, кидаем исключение
            else:
                et = """Value in RequestNode not initialized.
                        External values="""+str(values)+', inner value='+self._value if self._value else str(self._variable)
                logging.debug(et)
                raise Exception(et)
        if isinstance(val, dict):
                    #if dictionary with single value
                    if len(val) == 1: val = next(iter(val.values()))
        return val

    def get_node_required_keys(self):
        return ['plugin', 'reference']
