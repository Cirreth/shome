__author__ = 'cirreth'

import os
import importlib
import logging
from core.entities.Plugin import Plugin


class Performer:

    """
        There are few plugin states:
            1. Found, configured, active - can be used in processes
            2. Found, configured, inactive - can't be used until activated
            3. Not found, configured, active - error, user notification, PANIC!!!
            4. Not found, configured, inactive - unable to activate, user notification
            5. Found, not configured - allow to config it
    """

    #_plugins = {}
    #_known = {}
    #_error = {}

    #_configuration = None

    def init(self, context):
        logging.debug("Performer initialization")
        self._config = context.config

    def reload_plugins(self):
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
        return [name for name in self._plugins]

    def list_all_plugins(self):
        allplugins = []
        for p in self._plugins:
            allplugins.append(
                {
                    'name': p,
                    'params': self._known[p]['params'] if p in self._known else '',
                    'enabled': self._known[p]['enabled'] if p in self._known else '',
                    'status': 'active',
                }
            )
        for p in self._error:
            allplugins.append(
                {
                    'name': p,
                    'status': 'error',
                    'params': self._known[p]['params'] if p in self._known else '',
                    'enabled': self._known[p]['enabled'] if p in self._known else '',
                    'message': self._error[p]
                }
            )
        return allplugins

    def scan_plugins_folder(self):
        res = {'found': {}, 'error': {}}
        for plugin in os.listdir('plugins'):
            if not plugin.startswith('__') and not plugin.endswith('.py'):  # folders only
                for module in os.listdir('plugins/'+plugin):
                    if not module.startswith('__'):
                        try:
                            module_name = module[:-3]  # -py
                            m = importlib.import_module('plugins.'+plugin+'.'+module_name)
                            res['found'][plugin] = getattr(m, module_name)
                        except Exception as e:
                            logging.error('Not loaded '+plugin+' - '+str(e))
                            res['error'][plugin] = str(e)
        return res

    def init_plugins(self):
        self._known = {
            p.name: {
                'params': p.get_params(),
                'enabled': p.enabled
            } for p in Plugin.get_all()}
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