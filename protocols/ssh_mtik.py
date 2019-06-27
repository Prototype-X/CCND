#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


import pexpect
import sys
import logging


class SSH(object):
    def __init__(self):
        self.cfg_device = {}
        self.cfg = str

    def activate(self):
        if not self.connect():
            return 'ERR'
        if not self.run_cmd():
            return 'ERR'
        self.output()
        return self.config()

    def deactivate(self):
        pass

    def load_data(self, cfg_device: dict):
        self.cfg_device = cfg_device
        if 'port' not in self.cfg_device:
            self.cfg_device['port'] = 22

    def connect(self):
        try:
            self.cfg = pexpect.run('ssh -p {port} {login}@{pwd} export'.format(port=self.cfg_device['port'],
                                                                               login=self.cfg_device['login'],
                                                                               pwd=self.cfg_device['ip']),
                                   events={'(?i)password': '{}\n'.format(self.cfg_device['password']),
                                           '(?i)connecting (yes/no)?': 'yes\n'}, logfile=sys.stdout, echo=False)
            self.cfg = self.cfg.decode()
        except pexpect.ExceptionPexpect as err:
            print('ssh failed on login: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                      self.cfg_device['name'], err))
            return False
        return True

    def run_cmd(self):
        return True

    def output(self):
        pass

    def config(self):
        return self.cfg
