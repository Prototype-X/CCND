#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'

"""
For Dlink DES-1210
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
        self.cmd_backup = ''

    def run_cmd(self):
        self.cmd_backup = 'upload cfg_toTFTP tftp://{}/{}.cfg\n'.format(self.cfg_device['tftp_ip'], self.cfg_device['name'])

        try:
            self.telnet.write(self.cmd_backup)
            self.telnet.expect([self.prompt1, self.prompt2, pexpect.TIMEOUT], timeout=15)
        except (pexpect.TIMEOUT, pexpect.ExceptionPexpect) as err:
            print('telnet failed run command: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                            self.cfg_device['name'], err))
            return False
        return True


def setup():
    return Dlink()
