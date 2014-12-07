__author__ = 'Кирилл'

import os
import sys
import importlib
from plugins.SHomePlugin import SHomePlugin
import logging
"""
#plugins!
self.performer.add_plugin('onewire', OneWirePlugin('192.168.1.2', 4304))
self.performer.add_plugin('sysexec', SystemExecPlugin())
#self.performer.add_plugin('old_db', DatabaseMySQLPlugin('192.168.1.2', 'dev', 'dev', 'tcontrol'))
#self.performer.add_plugin('shome_db', DatabaseMySQLPlugin('192.168.1.2', 'dev', 'dev', 'shome'))
self.performer.add_plugin('delay', DelayPlugin())
self.performer.add_plugin('procexec', ProcessExecPlugin(self.action_processor))
self.performer.add_plugin('scheduler', SchedulerControlPlugin(self.scheduler))
self.performer.add_plugin('ledstrip', LedStripPlugin())
#self.performer.add_plugin('onewire', OneWirePlugin('25.196.219.36', 4304))
#end
"""

class Performer:

    """
        There are few plugin states:
            1. Found, configured, active - can be used in processes
            2. Found, configured, inactive - can't be used until activated
            3. Not found, configured, active - error, user notification, PANIC!!!
            4. Not found, configured, inactive - unable to activate, user notification
            5. Found, not configured - allow to config it
            6. Not found, not configured - you nothing know about it
    """

    _plugins = {}

    _new = {}
    _known = {}
    _found = {}
    _error = {}

    _configuration = None

    def init(self, context):
        logging.debug("Performer initialization")
        self._configuration = context.config
        self.init_plugins()

    def call(self, plugin, reference, values):
        if not plugin in self._plugins:
            msg = 'Plugin '+plugin+' is not found.'
            logging.error(msg)
            raise Exception(msg)
        res = self._plugins[plugin].call(reference, values)
        logging.debug("Value "+str(res)+" recieved")
        return res

    def add_plugin(self, name, plugin: "Initialized plugin instance"):
        logging.debug('Plugin instance with name '+plugin.getname()+' added as '+name)
        self._plugins[name] = plugin

    def list_loaded_plugins(self):
        return self._plugins.keys()

    def scan_plugins_folder(self):
        res = {'found': {}, 'error': {}}
        for plugin in os.listdir('plugins'):
            if not plugin.startswith('__') and not plugin.endswith('.py'): #folders only
                for module in os.listdir('plugins/'+plugin):
                    if not module.startswith('__'):
                        try:
                            module_name = module[:-3]
                            m = importlib.import_module('plugins.'+plugin+'.'+module_name)
                            res['found'][plugin] = getattr(m, module_name)
                        except Exception as e:
                            logging.error('Not loaded '+plugin+' - '+str(e))
                            res['error'][plugin] = str(e)
        return res

    def init_plugins(self):
        self._known = {p['name']: {'params': p['params'], 'enabled': p['enabled']} for p in self._configuration.get_all_plugins()}
        scanres = self.scan_plugins_folder()
        self._found = scanres['found']
        self._error = scanres['error']
        for fp in self._found:
            for kp in self._known:
                if fp == kp:
                    try:
                        self._plugins[kp] = self._found[kp](self._known[kp]['params'])
                    except Exception as e:
                        self._error[kp] = str(e)
        logging.info('initialized successfully: '+str(self._plugins))
        logging.info('found plugins: '+str(self._found))
        logging.info('not loaded plugins: '+str(self._error))