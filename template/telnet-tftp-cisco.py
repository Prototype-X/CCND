#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


"""
For Dlink DGS1510
Get config: upload config to tftp server
Transport: telnet
"""


import pexpect
from protocols.telnet import Telnet
import re


class Cisco(Telnet):
    def __init__(self):
        super(Cisco, self).__init__()
        self.cmd_copy = ''
        self.cmd_tftp = ''
        self.cmd_fname = ''
        self.prompt = None

    def run_cmd(self):
        try:
            self.cmd_copy = 'copy running-config tftp:\n'
            self.telnet.write(self.cmd_copy)
            self.prompt = re.compile(r'Address or name of remote host.*')
            self.telnet.expect([self.prompt, pexpect.TIMEOUT], timeout=10)

            self.cmd_tftp = '{}\n'.format(self.cfg_device['tftp_ip'])
            self.telnet.write(self.cmd_tftp)
            self.prompt = re.compile(r'Destination filename.*')
            self.telnet.expect([self.prompt, pexpect.TIMEOUT], timeout=10)

            self.cmd_fname = '{}.cfg\n'.format(self.cfg_device['name'])
            self.telnet.write(self.cmd_fname)
            self.prompt = re.compile(r'.*bytes copied in.*')
            self.telnet.expect([self.prompt, pexpect.TIMEOUT], timeout=10)
        except (pexpect.TIMEOUT, pexpect.ExceptionPexpect) as err:
            print('telnet failed run command: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                            self.cfg_device['name'], err))
            return False
        return True


def setup():
    return Cisco()
