#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


"""
For Mikrotik
Get config: grab output from CLI
Transport: ssh
"""


import logging
from protocols.ssh_mtik import SSH
import re
import pexpect


class Mikrotik(SSH):
    def __init__(self):
        super(Mikrotik, self).__init__()
        self.backup_regexp = re.compile(r'#(.*\s*)+')

    def config(self):
        self.cfg = self.cfg.replace('\r\r\n', '\r\n')
        reg = self.backup_regexp.search(self.cfg)
        if reg:
            self.cfg = reg.group()
        else:
            self.cfg = None
        return self.cfg


def setup():
    return Mikrotik()
