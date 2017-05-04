#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


"""
For Edge-Core ECS3510, ECS4610, ECS4510, ECS2100, 
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
            self.cmd_copy = 'copy running-config tftp\n'
            self.ssh.write(self.cmd_copy)
            self.prompt = re.compile(r'TFTP server IP address:.*')
            self.ssh.PROMPT = self.prompt
            self.ssh.prompt()

            self.cmd_tftp = '{}\n'.format(self.cfg_device['tftp_ip'])
            self.ssh.write(self.cmd_tftp)
            self.prompt = re.compile(r'Destination file name:.*')
            self.ssh.PROMPT = self.prompt
            self.ssh.prompt()

            self.cmd_fname = '{}.cfg\n'.format(self.cfg_device['name'])
            self.ssh.write(self.cmd_fname)
            self.prompt = re.compile(r'Success\.')
            self.ssh.PROMPT = self.prompt
            self.ssh.prompt()
        except pxssh.ExceptionPxssh as err:
            print('ssh failed run command: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                         self.cfg_device['name'], err))
            return False
        return True


def setup():
    return EdgeCore()
