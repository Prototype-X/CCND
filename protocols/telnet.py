#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


import pexpect
import sys
import time
import logging


class TelnetException(Exception):
    pass


class Telnet(object):
    def __init__(self):
        self.cfg_device = {}
        self.telnet = None
        self.cfg = str

    def activate(self):
        if not self.connect():
            return 'ERR'
        if not self.run_cmd():
            return 'ERR'
        self.output()
        return self.config()

    def deactivate(self):
        self.telnet.close()

    def load_data(self, cfg_device: dict):
        self.cfg_device = cfg_device
        if 'port' not in self.cfg_device:
            self.cfg_device['port'] = 23

    def connect(self):
        try:
            self.telnet = pexpect.spawn('telnet', [self.cfg_device['ip'], str(self.cfg_device['port'])],
                                        logfile=sys.stdout, encoding='utf-8', timeout=20)
            self.telnet.expect(['UserName:', 'username:', 'Username:', 'login:'], timeout=10)
            self.telnet.write('{}\n'.format(self.cfg_device['login']))
            time.sleep(1.0)
            self.telnet.expect(['PassWord:', 'password:', 'Password:'], timeout=10)
            self.telnet.write('{}\n'.format(self.cfg_device['password']))
            time.sleep(2.0)

        except (pexpect.TIMEOUT, pexpect.ExceptionPexpect) as err:
            print('telnet failed on login: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                         self.cfg_device['name'], err))
            return False
        return True

    def run_cmd(self):
        pass

    def output(self):
        pass

    def config(self):
        return True
