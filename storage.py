#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'

import os
from datetime import datetime
from shutil import copy2, make_archive, rmtree
import logging
logger = logging.getLogger('CCND')


class FileStorage(object):
    def __init__(self, path):
        # self.path = store_init['id']
        # self.type = store_init['type']
        self.dir_root = path
        self.dir_session = None
        self.path_session = None
        logger.info('Init file storage')

    def add_to_storage(self, fname, data):
        with open(self.path_session + '/' + fname + '.cfg', 'w') as file:
            file.write(data)

    def add_to_storage_from_tftp(self, fname, path_to_tftp):
        tftp = path_to_tftp + '/' + fname + '.cfg'
        storage = self.path_session + '/' + fname + '.cfg'
        try:
            copy2(tftp, storage)
            os.remove(tftp)
        except FileNotFoundError as err:
            print(err)
            return False
        return True

    def new_session(self):
        self.dir_session = 'backup-{}'.format(datetime.now().strftime("%Y-%m-%dT%H:%M"))
        self.path_session = '{}/{}'.format(self.dir_root, self.dir_session)
        os.makedirs(self.path_session, exist_ok=True)

    def close_session(self):
        self.archive()
        self.path_session = None

    def archive(self):
        make_archive(self.path_session, 'gztar', self.dir_root, self.dir_session)
        rmtree(self.path_session)


class GitStorage(object):
    def __init__(self, path):
        self.dir_root = path
        self.dir_session = None
        self.path_session = None
        logger.info('Init file storage')

    def add_to_storage(self, fname, data):
        pass

    def add_to_storage_from_tftp(self, fname, path_to_tftp):
        tftp = path_to_tftp + '/' + fname + '.cfg'
        storage = self.path_session + '/' + fname + '.cfg'
        try:
            copy2(tftp, storage)
            os.remove(tftp)
        except FileNotFoundError as err:
            print(err)
            return False
        return True

    def new_session(self):
        self.dir_session = 'backup-{}'.format(datetime.now().strftime("%Y-%m-%dT%H:%M"))
        self.path_session = '{}/{}'.format(self.dir_root, self.dir_session)
        os.makedirs(self.path_session, exist_ok=True)

    def close_session(self):
        self.path_session = None
