#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


"""
For Dlink DES-3526, DES-3528, DES-3552, DGS-3426G
Get config: grab output from CLI
Transport: telnet
"""


import logging
from protocols.telnet import Telnet
import re
import pexpect


class Dlink(Telnet):
    def __init__(self):
        self.cmd_pre = 'disable clipaging \n'
        self.cmd_backup = 'show config current_config \n'
        self.cmd_post = 'enable clipaging \n'
        self.backup_regexp = re.compile(r'#-(.*\s*)+--')
        self.prompt = re.compile(r'(.{1,16}):(.{1,15}#)$')
        # self.prompt = re.compile(r'(.+):(.+)#')
        super(Dlink, self).__init__()

    def run_cmd(self):
        try:
            if self.cmd_pre:
                self.telnet.write(self.cmd_pre)
                self.telnet.expect(self.prompt)

            if self.cmd_backup:
                self.telnet.write(self.cmd_backup)
                self.telnet.expect(self.prompt)

            if self.cmd_post:
                self.telnet.write(self.cmd_post)
                self.telnet.expect(self.prompt)
        except (pexpect.TIMEOUT, pexpect.ExceptionPexpect) as err:
            print('telnet failed run command: IP {}, Host {}, Err{}'.format(self.cfg_device['ip'],
                                                                            self.cfg_device['name'], err))
            return False
        return True

    def config(self):
        self.cfg = self.cfg.replace('\r', '')
        reg = self.backup_regexp.search(self.cfg)
        if reg:
            self.cfg = reg.group()
        else:
            self.cfg = None
        return self.cfg

    def output(self):
        self.cfg = self.telnet.before


def setup():
    return Dlink()
