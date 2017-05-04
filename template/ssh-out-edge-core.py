#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


"""
For Edge-Core ECS3510, ECS4610, ECS4510, ECS2100, ES3552M, 
Get config: grab output from CLI
Transport: ssh
"""


import logging
from protocols.ssh import SSH
import re
from pexpect import pxssh


class EdgeCore(SSH):
    def __init__(self):
        self.cmd_pre = 'terminal length 0\nterminal width 300\n'
        self.cmd_backup = 'show running-config\n'
        self.cmd_post = ''
        self.backup_regexp = re.compile(r'!(.*\s*)+end')
        self.prompt = re.compile(r'Vty-\d{1,2}#$')
        super(EdgeCore, self).__init__()
        self.ssh.PROMPT = self.prompt

    def run_cmd(self):
        try:
            if self.cmd_pre:
                self.ssh.write(self.cmd_pre)
                self.ssh.prompt()

            if self.cmd_backup:
                self.ssh.write(self.cmd_backup)
                self.ssh.prompt()

            if self.cmd_post:
                self.ssh.write(self.cmd_post)
                self.ssh.prompt()
        except pxssh.ExceptionPxssh as err:
            print('ssh failed run command: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                         self.cfg_device['name'], err))
            return False
        return True

    def output(self):
        self.cfg = self.ssh.before

    def config(self):
        reg = self.backup_regexp.search(self.cfg)
        if reg:
            self.cfg = reg.group()
        else:
            self.cfg = None
        return self.cfg


def setup():
    return EdgeCore()
