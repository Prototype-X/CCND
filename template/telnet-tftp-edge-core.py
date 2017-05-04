#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


"""
For Edge-Core ECS3510, ECS4610, ECS4510, ECS2100, ES3552M, 
Get config: upload config to tftp server
Transport: telnet
"""


import logging
from protocols.telnet import Telnet
import re
import pexpect


class EdgeCore(Telnet):
    def __init__(self):
        super(EdgeCore, self).__init__()
        self.cmd_copy = ''
        self.cmd_tftp = ''
        self.cmd_fname = ''
        self.prompt = None

    def run_cmd(self):

        try:
            self.cmd_copy = 'copy running-config tftp\n'
            self.telnet.write(self.cmd_copy)
            self.prompt = re.compile(r'TFTP server IP address:.*')
            self.telnet.expect([self.prompt, pexpect.TIMEOUT], timeout=10)

            self.cmd_tftp = '{}\n'.format(self.cfg_device['tftp_ip'])
            self.telnet.write(self.cmd_tftp)
            self.prompt = re.compile(r'Destination file name:.*')
            self.telnet.expect([self.prompt, pexpect.TIMEOUT], timeout=10)

            self.cmd_fname = '{}.cfg\n'.format(self.cfg_device['name'])
            self.telnet.write(self.cmd_fname)
            self.prompt = re.compile(r'Success\.')
            self.telnet.expect([self.prompt, pexpect.TIMEOUT], timeout=10)
        except (pexpect.TIMEOUT, pexpect.ExceptionPexpect) as err:
            print('telnet failed run command: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                            self.cfg_device['name'], err))
            return False
        return True


def setup():
    return EdgeCore()
