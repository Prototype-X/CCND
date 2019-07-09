#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


"""
For ELTEX MES switches
Get config: upload config to tftp server
Transport: ssh
"""


import logging
from protocols.ssh import SSH
import re
from pexpect import pxssh


class EdgeCore(SSH):
    def __init__(self):
        super(EdgeCore, self).__init__()
        self.cmd_copy = ''
        self.cmd_tftp = ''
        self.cmd_fname = ''
        self.prompt = None

    def run_cmd(self):
        try:
            self.cmd_copy = 'copy running-config tftp://{ip}/{name}.cfg\n'.format(ip=self.cfg_device['tftp_ip'],
                                                                                  name=self.cfg_device['name'])
            self.ssh.write(self.cmd_copy)
            self.prompt = re.compile(r'Copy:.*bytes copied in.*')
            self.ssh.PROMPT = self.prompt
            self.ssh.prompt()
        except pxssh.ExceptionPxssh as err:
            print('ssh failed run command: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                         self.cfg_device['name'], err))
            return False
        return True


def setup():
    return EdgeCore()
