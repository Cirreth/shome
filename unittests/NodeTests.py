import logging

__author__ = 'Кирилл'

import unittest
import json
from core.actproctree import *

class MyTestCase(unittest.TestCase):

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

    def test_request_node(self):
        #simple ow address
        ow0 = '{"type": "RequestNode", "plugin": "onewire", "address": "/28.F2CF39040000/temperature"}'
        owj0 = MyTestCase.prepare(ow0)
        own0 = RequestNode(owj0)
        self.assertEqual('onewire', own0._plugin)
        self.assertEqual('/28.F2CF39040000/temperature', own0._address)

    def test_action_node(self):
        #
        #simple ow action record with static value
        ow0 = '{"type": "ActionNode", "plugin": "onewire", "address": "/3A.C9330D000000/PIO.A", "value": 1}'
        owj0 = MyTestCase.prepare(ow0)
        own0 = ActionNode(owj0)
        self.assertEqual('onewire', own0._plugin)
        self.assertEqual('/3A.C9330D000000/PIO.A', own0._address)
        self.assertEqual(1, own0._value)
        #
        #simple ow action record with variable
        ow0 = '{"type": "ActionNode", "plugin": "onewire", "address": "/3A.C9330D000000/PIO.A", "variable": "v"}'
        owj0 = MyTestCase.prepare(ow0)
        own0 = ActionNode(owj0)
        self.assertEqual('onewire', own0._plugin)
        self.assertEqual('/3A.C9330D000000/PIO.A', own0._address)
        self.assertEqual('v', own0._variable)

    def test_expression_node(self):
        pass

    def test_conditional_node(self):
        #
        #   типы операндов:
        #       RequestNode snippet     - имя узла, который полностью будет описан в секции snippets
        #       ConditionalNode snippet - имя узла, который полностью будет описан в секции snippets
        """     !IDEA ActionNode может вести себя подобно RequestNode, поэтому его можно(?) использовать в условиях
                 !то есть его можно считать "Узлом, возвращающим значение"                                           """
        #       RequestNode link        - ссылка на существующий процесс, состоящий из RequestNode
        #       Conditional link        - ссылка еа существующий процесс, в корне которого ConditionalNode
        #       переменные              - строки, не заключенные в кавычки, значения которых не найдены в словарях выше
        #       значения                - числа и строки в одинарных или двойных кавычках
        #
        #########
        #
        #simple one wire comparison operator
        ow0 = """{"type": "ConditionalNode", "condition": "t1 > tlow",
                "snippets": {
                   "t1": {"type": "RequestNode", "plugin": "onewire", "address": "/28.F2CF39040000/temperature"}
                }}"""
        owj0 = MyTestCase.prepare(ow0)
        own0 = ConditionalNode(owj0)
        self.assertEqual('t1 > tlow', own0._condition)
        print(own0.execute({'tlow': 20}))

    def prepare(ci):
        return {k: json.dumps(v) for k, v in json.loads(ci).items()}

if __name__ == '__main__':
    unittest.main()
