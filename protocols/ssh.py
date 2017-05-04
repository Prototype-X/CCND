#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


from pexpect import pxssh
import sys
import os
import logging


class SSHException(Exception):
    pass


class SSH(object):
    def __init__(self):
        self.cfg_device = {}
        self.ssh = pxssh.pxssh(logfile=sys.stdout, encoding='utf-8', timeout=30, echo=False)
        self.cfg = str

    def activate(self):
        if not self.connect():
            return 'ERR'
        if not self.run_cmd():
            return 'ERR'
        self.output()
        return self.config()

    def deactivate(self):
        self.ssh.logout()

    def load_data(self, cfg_device: dict):
        self.cfg_device = cfg_device

    def connect(self):
        try:
            ok = self.ssh.login(self.cfg_device['ip'], self.cfg_device['login'],
                                password=self.cfg_device['password'], auto_prompt_reset=False, login_timeout=20)
            return ok
        except pxssh.ExceptionPxssh as err:
            print('ssh failed on login: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                      self.cfg_device['name'], err))
            return False

    def run_cmd(self):
        pass

    def output(self):
        pass

    def config(self):
        return True
