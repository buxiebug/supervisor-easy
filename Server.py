# encoding:utf8
__author__ = 'brianyang'

import time
import xmlrpclib
from uuid import uuid4
import logging


class Server(object):
    def __init__(self, host, port, user, password, name=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.id = str(uuid4())
        self.RUNNING = 20
        self.STARTING = 10
        self.STOPPED = 0
        if name:
            self.name = name
        else:
            self.name = '%s@%s:%d' % (self.user, self.host, self.port)
        self.rpc_proxy = xmlrpclib.Server('http://%s:%s@%s:%d/RPC2' % (self.user, self.password, self.host, self.port))

    def get_process_info(self, app_name):
        process_info = {}
        try:
            process_info = self.rpc_proxy.supervisor.getProcessInfo(app_name)
        except Exception, e:
            logging.error(e)

        process_info['host'] = self.host
        process_info['port'] = self.port
        process_info['user'] = self.user
        process_info['id'] = self.id
        return process_info

    def get_all_process_info(self):
        process_infos = self.rpc_proxy.supervisor.getAllProcessInfo()
        for process_info in process_infos:
            process_info['host'] = self.host
            process_info['port'] = self.port
            process_info['user'] = self.user
            process_info['id'] = self.id
        return process_infos

    def stop_process(self, app_name):
        if self.check_status(app_name, self.STARTING, self.RUNNING):
            return self.rpc_proxy.supervisor.stopProcess(app_name)
        return True

    def start_process(self, app_name):
        if self.check_status(app_name, self.STOPPED):
            return self.rpc_proxy.supervisor.startProcess(app_name)
        return True

    def restart_process(self, app_name):
        self.stop_process(app_name)
        return self.start_process(app_name)

    def check_status(self, app_name, *args):
        process_info = self.get_process_info(app_name)
        state = process_info.get('state')
        if state not in args:
            return False
        return True

    def restart_all_apps(self):
        f1 = self.rpc_proxy.supervisor.stopAllProcesses()
        f2 = self.rpc_proxy.supervisor.startAllProcesses()
        return f1 and f2

    def start_all_apps(self):
        return self.rpc_proxy.supervisor.startAllProcesses()

    def stop_all_apps(self):
        return self.rpc_proxy.supervisor.stopAllProcesses()

    def tail_log(self, app_name, format_func):
        offset = 0
        func = self.rpc_proxy.supervisor.tailProcessLog
        while True:
            log, offset, ret = func(app_name, offset, 1000)
            time.sleep(0.5)
            for log in log.split('\n'):
                yield format_func(log)
