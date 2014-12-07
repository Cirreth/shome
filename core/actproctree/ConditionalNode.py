import json
import logging

__author__ = 'Кирилл'
from core.actproctree.AbstractNode import AbstractNode
import re

class ConditionalNode(AbstractNode):

    _condition = None
    _variables = {}
    #
    _yes = None
    _no = None
    _retvar = None

    def __init__(self, process_tag, structure):
        super().__init__(process_tag, structure)
        logging.debug('Conditional node constructing...')

    def __build__(self):
        """
        1. Установить condition
        2. Создать узлы со сниппетами
        3. Сохранить retvar
        """
        self._condition = self._structure['condition'][1:-1]
        if 'variables' in self._structure:
            vars = json.loads(self._structure['variables'])
            for v in vars:
                if isinstance(v, dict):
                    self._variables.update(v)
        self._yes = self.create_direction('yes')
        self._no = self.create_direction('no')
        self._next = self.create_direction('next')
        self._parallel = self.create_direction('parallel')
        self._exceptional = self.create_direction('exceptional')
        if 'retvar' in self._structure:
            self._retvar = self._structure['retvar'][1:-1]

    def execute(self, values={}):
        """
        1. Заменить плейсхолдеры
            1.1 Из values
            1.2 Из глобальный переменных процесса
        2. Вычислить условие
        """
        self.execute_direction(self._parallel, values)
        logging.debug('Condition before evaluation: '+self._condition)
        condition = self.__prepare_conditon(values)
        logging.debug('Condition to evaluate: '+condition)
        res = eval(condition)
        logging.debug('Evaluation result: '+str(res))
        if self._retvar:
            self._action_processor.pss_variables[self._process_tag][self._retvar] = res
        res_proc = []
        if self._parallel:
            res_proc.extend(self._parallel)
        if res:
            if self._yes:
                res_proc.extend(self._yes)
            self.execute_direction(res_proc, values)
        else:
            if self._no: res_proc.extend(self._no)
            self.execute_direction(res_proc, values)
        self.execute_direction(self._parallel, values)
        self.execute_direction(self._next, values)
        return res

    def __prepare_conditon(self, values):
            """Заменяет токены в ссылке на их текущие значения"""
            pvars = self._action_processor.pss_variables
            ref = ''
            lst = 0
            tknval = None
            for c in re.finditer('<[a-zA-Z0-9]+?>', self._condition):
                name = c.group(0)[1:-1] #variable name
                #looking for value
                if not isinstance(values, dict):
                    raise Exception('Неверный тип параметра values ('+values+')')
                if name in values:
                    tknval = values[name]
                elif self._process_tag in pvars and name in pvars[self._process_tag]:
                    tknval = pvars[self._process_tag][name]
                elif name in self._variables:
                    tknval = self._variables[name]
                if not tknval is None:
                    if isinstance(tknval, dict) and len(tknval) == 1:
                        tknval = next(iter(tknval.values()))
                    ref += self._condition[lst:c.start(0)]+str(tknval)
                lst = c.end(0)
            ref += self._condition[lst:]
            return ref

    def get_node_required_keys(self):
        return ['condition']