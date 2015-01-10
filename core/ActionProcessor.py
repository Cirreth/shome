__author__ = 'cirreth'
from core.actproctree import *
from core.exceptions.InvalidNodeTypeException import InvalidNodeTypeException
from core.exceptions.ParsingException import ParsingException
from threading import Thread
import json
import re
import logging


class ActionProcessor:

    _performer = None
    # processes dictionary
    _processes = {}
    # processes string representations
    _processes_str = {}
    # config storage
    _configuration = None
    # processes variable
    pss_variables = {}
    # deny executing for
    deny_exec = []
    # active threads
    active_threads = None

    def __init__(self):
        pass

    def init(self, context):
        logging.debug("Action processor initialization")
        self._performer = context.performer
        if not context.performer:
            raise Exception('Performer is null')
        AbstractNode._performer = context.performer
        AbstractNode._scheduler = context.scheduler
        AbstractNode._action_processor = self
        self._configuration = context.config

    def list_all(self):
        return [
            {
                'name': p
            }
            for p in self._processes
        ]

    def get_process(self, name):
        if name in self._processes_str:
            return self._processes_str[name]
        else:
            return 'Process is not found'

    def find_process_usages(self, name):
        res = []
        for p in self._processes_str:
            if name in self._processes_str[p]:
                res.append(p)
        return res

    def delete_process(self, name):
        """
            Delete process from ActionProcessor.
            Raise exception if process is used in other process.
        """
        if name in self._processes_str:
            procusgs = self.find_process_usages(name)
            if len(procusgs) > 0:
                raise Exception('Process are used in ['+', '.join(procusgs) +
                                ']. Delete or modify related processes.')
            self._configuration.delete_process(name)
            del self._processes_str[name]
            del self._processes[name]
            if name in self.pss_variables:
                del self.pss_variables[name]

    def update_proc_var(self, tag, name, value):
        if tag not in self.pss_variables:
            self.pss_variables[tag] = {}
        self.pss_variables[tag][name] = value

    def process(self, message, queue=None, message_id=None):
        """
            1. Parameter 'message' checking for tag{values} format accordance
            2. Find requested tag in _processes and execute it.

            If queue and message_id passed to the function, method will run new thread.
            Evaluation result will be placed in queue in format {message_id: result}
            If queue or message_id skipped, result will be evaluated in current thread
            and result will be returned by return operator
        """
        def process_wrapper(message, queue=None, message_id=None):
            logging.debug('process wrapper with ( '+message+' )')
            tag_values = parse_command(message)
            if tag_values:
                variables = {}
                tag = tag_values[0]
                values = tag_values[1]
                if tag in self._processes:
                    if tag in self.deny_exec:
                        logging.error(message+' ignored cause already running.')
                        raise Exception('Process '+tag+' already running')
                    logging.info('Process '+message+' executed')
                    if values:
                        splitted_values = self.split_parameters(values)
                        splitted = self.separate_values(splitted_values)
                        for k in splitted:
                            variables[k] = prepare_parameter(splitted[k])
                    # when few processes on one level
                    if isinstance(self._processes[tag], list):
                        self.deny_exec.append(tag)
                        threads = [Thread(target=e.execute, args=(variables, )) for e in self._processes[tag]]
                        logging.debug(str(len(threads)) + ' threads executed in process ( '+tag+' )')
                        for t in threads:
                            t.start()
                        for t in threads:
                            t.join()
                        self.deny_exec.remove(tag)
                    else:
                        self.deny_exec.append(tag)
                        t = Thread(target=self._processes[tag].execute, args=(variables, ))
                        logging.debug('thread executed in process ( '+tag+' )')
                        t.start()
                        t.join()
                        self.deny_exec.remove(tag)
                    if queue and message_id:
                        if tag in self.pss_variables:
                            queue.put(self.pss_variables[tag])
                        else:
                            queue.put('recieved')
                    return self.pss_variables[tag] if tag in self.pss_variables else None
                else:
                    logging.info('Process with tag '+tag+' is not found')
                    if queue and message_id:
                        queue.put(message_id+':::::'+'process is not found')
                    else:
                        return 'Process is not found'
            else:
                logging.info('String ( '+message+' ) is not command')
                return "Message ( "+message+" ) has been ignored"
        #
        message = message.strip()
        logging.debug('ActionProcessor process method call with message ( '+message+' )')
        if queue and message_id:
            logging.debug('action processor process method call in new thread')
            Thread(target=process_wrapper, args=(message, queue, message_id)).start()
        else:
            logging.debug('action processor process method call in the same thread')
            return process_wrapper(message)

    @staticmethod
    def separate_values(values):
        # TODO Test
        """
        in ['v=1', "z='asdsad'"]
        out [{'v': 1},{'z': 'asdsad'}]
        """
        # TODO .strip("'") for parameter in next line?
        return {p[0:p.find('=')]: p[p.find('=')+1:] for p in values}

    @staticmethod
    def split_parameters(string):
        # TODO not working on a=1, b=' =_= hello, my \'friends\''
        res = []
        lock = False
        cur = 0
        last = 0
        for c in string:
            if c == ',' and not lock:
                res.append(string[last:cur])
                last = cur+1
            elif c == "'" and string[cur-1] != "\\":
                lock = not lock
            cur += 1
        res.append(string[last:])
        logging.debug('splitted on' + str(res))
        return [p.strip() for p in res]

    def create_process(self, tag, expression, writedb=False):
        """
            Build process tree, add root element to _processes
        """
        if tag in self._processes:
            raise Exception('Process ('+tag+') already exists')
        try:
            self._processes[tag] = self.build_process_tree(tag, expression)
            self._processes_str[tag] = expression
            if writedb:
                try:
                    self._configuration.add_process(tag, expression)
                except Exception as se:
                    return 'Process tag created, but config update failed. '+str(se)
            return 'Process '+tag+' created successfully'
        except Exception as e:
            logging.error(e)
            raise e

    def update_process(self, tag, expression):
        if tag not in self._processes:
            return 'Process does not exist'
        self._processes[tag] = self.build_process_tree(tag, expression)
        self._processes_str[tag] = expression
        try:
            self._configuration.update_process(tag, expression)
        except Exception as se:
            return 'Process tag created, but config update failed. '+str(se)
        return 'Process '+tag+' updated successfully'

    def build_process_tree(self, tag, expression):
        """
            Returns tree node
        """
        # TODO Processing in transaction required
        logging.debug('Begin building expression tree with ( '+expression+' )')
        #
        root_struct = parse_level(expression)
        if isinstance(root_struct, list):
            return [create_node(tag, n) for n in root_struct]
        elif 'type' not in root_struct:
            raise ParsingException
        return create_node(tag, root_struct)

    def create_node_direction(self, tag, expression):
        expression = expression.strip()
        try:
            structure = parse_level(expression)
            #{...}/[...] = > node/[node, node, ...]
            if isinstance(structure, dict):
                res = [create_node(tag, structure)]
                structure = res
            elif isinstance(structure, list):
                for i in range(0, len(structure)):
                    structure[i] = create_node(tag, structure[i])
        except ValueError:
            structure = []
            if expression[0] == '[':
                lbllist = [i.strip() for i in expression[1:-1].split(',')]
                for label in lbllist:
                    node = self.get_node_with_label(tag, label)
                    if node:
                        structure.append(node)
                    else:
                        structure.append(label)  # process existing checking required?
            else:
                node = self.get_node_with_label(tag, expression)
                if node:
                    structure.append(node)
                else:
                    structure.append(expression)
        return structure

def parse_command(message):
        """
        Parse command to split it to two parts: process name and execution parameters
        Returns tuple
            (tag,None), if command contains address only,
            (tag,dic), if parameters provided
            else False
        """
        logging.debug('ActionProcessor: parsing message( '+message+' )')
        cmd = re.compile('^([^{}]+)\{([^{}]+)\}$').search(message)
        if cmd:
            logging.debug('Message matched as command '+cmd.group(1)+' with values '+cmd.group(2))
            return cmd.group(1), cmd.group(2)
        else:
            cmd = re.compile('^[^{}]+$').search(message)
            if cmd:
                logging.debug('Message matched as command '+cmd.group(0)+' without value ')
                return cmd.group(0), None
        raise Exception(message + 'not matched by regex ^([^{}]+)\{([^{}]+)\}$')

def create_node(tag, structure):
    logging.debug('create node decomposition result: '+str(structure))
    node_type = structure['type'][1:-1]
    if node_type == 'RequestNode':
        return RequestNode(tag, structure)
    elif node_type == 'SchedulerNode':
        return SchedulerNode(tag, structure)
    elif node_type == 'ExecuteNode':
        return ExecuteNode(tag, structure)
    elif node_type == 'ConditionalNode':
        return ConditionalNode(tag, structure)
    elif node_type == 'DelayNode':
        return DelayNode(tag, structure)
    else:
        raise InvalidNodeTypeException


#  @TODO AbstractNode method duplicate!
def parse_level(ci):
    """
        Convert first structure level to json
    """
    if re.search('^\\s*\\[', ci):
        return [{k: json.dumps(v) for k, v in e.items()} for e in json.loads(ci)]
    else:
        return {k: json.dumps(v) for k, v in json.loads(ci).items()}


def prepare_parameter(parameter):
    """
        Convert parameter to python object.
        Convert: string to int/float if it is numeric, or delete wrapping quotes.
    """
    logging.debug('Prepairing parameter '+parameter+'...')
    if parameter[0] == "'" or parameter[0] == '"':
        logging.debug('...recognized as quoted string')
        return parameter[1:-1]
    try:
        logging.debug('...possible integer?..')
        return int(parameter)
    except ValueError:
        try:
            logging.debug('...or float?..')
            return float(parameter)
        except ValueError:
            logging.debug('neither digit nor quoted string')
            return parameter


def prepare_parameters(parameters):
    return {k: prepare_parameter(parameters[k]) for k in parameters}