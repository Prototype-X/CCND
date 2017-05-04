#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'

"""
For Dlink DGS-1100
Get config: upload config to tftp server
Transport: telnet
"""



import logging
import time
from protocols.telnet import Telnet
import re
import pexpect


class Dlink(Telnet):
    def __init__(self):
        super(Dlink, self).__init__()
        self.prompt1 = re.compile(r'Upload configuration.*Done.*')
        self.prompt2 = re.compile('Configuration backup Successfully')
        self.prompt3 = re.compile('\[OK]')
        self.prompt = re.compile(r'(.{1,16}):(.{1,15}#)$')
        self.cmd_pre = 'save config config_id 1\n'
        self.cmd_backup = ''

    def run_cmd(self):
        self.cmd_backup = 'upload cfg_toTFTP {} {}.cfg config_id 1\n'.format(self.cfg_device['tftp_ip'], self.cfg_device['name'])

        try:
            self.telnet.write(self.cmd_pre)
            self.telnet.expect([self.prompt3, self.prompt, pexpect.TIMEOUT], timeout=15)

            self.telnet.write(self.cmd_backup)
            self.telnet.expect([self.prompt1, self.prompt2, pexpect.TIMEOUT], timeout=15)
        except (pexpect.TIMEOUT, pexpect.ExceptionPexpect) as err:
            print('telnet failed run command: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                            self.cfg_device['name'], err))
            return False
        return True


def setup():
    return Dlink()
