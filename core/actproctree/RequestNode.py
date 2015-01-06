__author__ = 'cirreth'

from core.actproctree.AbstractNode import AbstractNode
from threading import Thread, active_count
import json
import queue
import logging

class RequestNode(AbstractNode):
    """Request value from plugin"""

    """Executive plugin name"""
    _plugin = None
    """Unique identifier will be sended to executive plugin"""
    _reference = None
    """if _retval is setted, request result will be saved in ActionProcessor proc. variables"""
    _retvar = None
    """Set the value or the variable, never both"""
    _value = None
    _variable = None

    def __init__(self, process_tag, structure):
        super().__init__(process_tag, structure)
        logging.debug('Request node constructing...')

    def __build__(self):
        self._plugin = self._structure['plugin'][1:-1]
        self._reference = self._structure['reference'][1:-1]
        if 'retvar' in self._structure:
            self._retvar = self._structure['retvar'][1:-1]
        #Ключ value определяет значение(переменную) которое будет передано как параметр для записи
        #"value": 1, "value": "'string'"    -   константы
        #"value": "x"   -   переменная, значение которой устанавливается во время вызова
        #"value": {"x":1}   -   переменная, проинициализированная значением по умолчанию
        #"variables": ["table", "rownum"]   -   не инициализированные переменные (заполняются None)
        #"variables": [{"table": \'temperature\'}, {"rownum":3}]    -   инициализированные переменные
        #Вытаскиваем все переменные
        if 'value' in self._structure:
            value = json.loads(self._structure['value'])
            if isinstance(value, dict):
                if len(value) == 1:
                    self._variable = value
                else:
                    logging.error('Dictionary {<varname>:<initial value>} used as variable must contain only one value')
                    raise Exception('Variable in RequestNode contains more (or less) than one key:value pair')
            elif isinstance(value, str):
                if value[0] == "'":
                    self._value = value[1:-1]
                else:
                    self._variable = {value: None}
            elif isinstance(value, int) or isinstance(value, float):
                self._value = value
        #
        if 'variables' in self._structure:
            vars = json.loads(self._structure['variables'])
            for v in vars:
                if isinstance(v, dict):
                    self._variables.update(v)
        self._next = self.create_direction('next')
        self._parallel = self.create_direction('parallel')
        self._exceptional = self.create_direction('exceptional')

    def execute(self, values={}):
        def execute_wrapper(plugin, ref, val, ret):
            ac = active_count()
            self._action_processor.active_threads = ac
            logging.info('Threads alive: ' + str(ac))
            try:
                res = AbstractNode._performer.call(plugin, ref, val)
            except Exception as e:
                res = str(e)
            ret.put(res)
            logging.debug('Thread with ref ( '+ref+' ) evaluation result: '+str(ret.queue[0])) #!!
        logging.debug('Executed RequestNode with reference ( '+self._reference+' )')
        ref = self.prepare_ref(self._reference, values)
        val = self.__prepare_value(values)
        #CALL NODE
        ret = queue.Queue()
        current_thread = Thread(target=execute_wrapper, args=(self._plugin, ref, val, ret))
        current_thread.start()
        #
        #CALL PARALLEL
        self.execute_direction(self._parallel, values)
        #
        logging.debug('current node thread joined to main')
        current_thread.join()
        if self._retvar:
            AbstractNode._action_processor.update_proc_var(self._process_tag, self._retvar, ret.get())
        logging.debug('All parallel nodes of process '+self._process_tag+' completed')
        #CALL NEXT
        self.execute_direction(self._next, values)
        logging.debug('All ways of '+self._reference+' completed')

    def __prepare_value(self, values):
        pvars = self._action_processor.pss_variables
        val = None  #will be used as value argument
        #Use value if setted
        if not self._value is None:
            val = self._value
        #...else variable name must be set
        elif self._variable:
            key = next(iter(self._variable.keys()))
            #looking for variable value in user set parameters
            if key in values:
                val = values[key]
            elif self._process_tag in pvars and key in pvars[self._process_tag]:
                val = pvars[self._process_tag][key]
            elif self._variable[key]:
                val = self._variable[key]
            else:
                et = """Value in RequestNode not initialized.
                        External values="""+str(values)+', inner value='+self._value if self._value else str(self._variable)
                logging.debug(et)
                raise Exception(et)
        if isinstance(val, dict):
                    #if dictionary with single value
                    if len(val) == 1:
                        val = next(iter(val.values()))
        return val

    def get_node_required_keys(self):
        return ['plugin', 'reference']
