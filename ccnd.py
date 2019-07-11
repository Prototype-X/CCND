#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'maximus'


import argparse
from shutil import copy2, make_archive, rmtree
from multiprocessing import Pool
import os
import sys
from datetime import datetime
import ruamel.yaml as yaml
from pluginbase import PluginBase
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('CCND')


class CCNDConfigYaml(object):
    def __init__(self, config_path_fn: str):
        self.config_path_fn = config_path_fn
        self.config = {}
        logger.info('Init CCND config')

    def load(self):
        with open(self.config_path_fn, 'r') as file:
            try:
                self.config = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        return self.config

    def save(self):
        pass

    def _save_config(self):
        pass


class HostConfigYaml(object):
    def __init__(self, config_path_fn: str, profile_path: str):
        self.config_path_fn = config_path_fn
        self.profile_path = profile_path
        self.config = {}
        self.profile = {}
        logger.info('Init ConfigManager')

    def load(self):
        with open(self.config_path_fn, 'r') as file:
            try:
                self.config = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        for self.name in self.config.keys():
            try:
                if self.config[self.name]['profile']:
                    with open(self.profile_path + self.config[self.name]['profile'], 'r') as profile:
                        self.profile = yaml.safe_load(profile)
                        self.config[self.name].update(self.profile)
            except KeyError:
                continue

        return self.config

    def save(self):
        pass

    def _save_config(self):
        pass

    def _save_profile(self):
        pass

    def filter_group(self):
        pass


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


class CliManager(object):
    def __init__(self):
        self.root_path = str(os.path.dirname(os.path.abspath(__file__)))
        self.template_path = self.root_path + '/template'
        self.host_path_fn = self.root_path + '/config/host.yaml'
        self.config_path_fn = self.root_path + '/config/config.yaml'
        self.profile_path = self.root_path + '/config/profile'
        self.storage_path = self.root_path + '/storage'

        self.parser = argparse.ArgumentParser(conflict_handler='resolve', description='CCND. The collector of '
                                                                                      'configurations for network '
                                                                                      'devices')
        self.parser.add_argument('-v', '--version', action='store_true', help='show version')
        self.parser.add_argument('-h', '--help', action='help', help='show help')
        self.parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')

        self.parser.add_argument('-c', '--cfg', nargs='+', action='store', type=str, help='Config file name and path')
        self.parser.add_argument('-p', '--profile', action='store', type=str, help='Profile path')
        self.parser.add_argument('--template', action='store', type=str, help='Template path')
        self.parser.add_argument('-s', '--storage', nargs='+', action='store', type=str, help='Storage')

        self.args = self.parser.parse_args()

        if not vars(self.args):
            self.parser.print_help()
            sys.exit()

        if self.args.version:
            print('CCND 0.2')
            sys.exit()

        if self.args.cfg:
            self.host_path_fn = self.args.cfg

        if self.args.profile:
            self.profile_path = self.args.profile

        if self.args.template:
            self.template_path = self.args.template

        self._cfg_logging()

    def _cfg_logging(self):
        """
        Configure logging output format.
        """
        if self.args.debug:
            loglevel = logging.DEBUG
        else:
            loglevel = logging.INFO
        logformat = '[%(asctime)s] [%(name)s:%(levelname)s] - %(message)s'
        logging.basicConfig(level=loglevel, format=logformat, datefmt='%d/%m/%Y %H:%M:%S')

    def get_params(self):
        return {'root_path': self.root_path, 'template_path': self.template_path,
                'host_path_fn': self.host_path_fn, 'profile_path': self.profile_path,
                'config_path_fn': self.config_path_fn, 'storage_path': self.storage_path}


class StorageManager(object):
    def __init__(self, path):
        # self.path = store_init['id']
        # self.type = store_init['type']
        self.dir_root = path
        self.dir_session = None
        self.path_session = None
        logger.info('Init StorageManager')

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


class BackupManager(object):
    def __init__(self, path):
        self.path = path
        self.stat = []
        # self.template_source = self._template_load()
        self.config = self._host_cfg_load()
        self.storage = StorageManager(self.path['storage_path'])
        logger.info('Init BackupManager')

    def _host_cfg_load(self):
        self.cfg_obj = HostConfigYaml(self.path['host_path_fn'], self.path['profile_path'])
        return self.cfg_obj.load()

    def _template_load(self):
        plugin = PluginBase(package='ccnd.plugins')
        return plugin.make_plugin_source(searchpath=[self.path['template_path']])

    def run(self):
        param_list = []
        for hostname, cfg in self.config.items():
            if not cfg['state']:
                continue
            cfg['name'] = hostname
            param_list.append((self.path['template_path'], cfg))
        # result = worker(param_list[0])
        # print(result)
        pool = Pool(processes=32)
        results = pool.map(func=worker, iterable=param_list)
        pool.close()
        pool.join()
        # exit()
        self.storage.new_session()
        for result in results:
            if self.config[result[0]]['storage'] in ('default', 'archive') and result[1] != 'ERR' and result[1] is not None:
                self.storage.add_to_storage(result[0], result[1])
            elif self.config[result[0]]['storage'] == 'tftp' and result[1] != 'ERR':
                if not self.storage.add_to_storage_from_tftp(result[0], self.config[result[0]]['tftp_path']):
                    self.stat.append('Error backup hostname: {} IP: {}'.format(result[0], self.config[result[0]]['ip']))
            else:
                self.stat.append('Error backup hostname: {} IP: {}'.format(result[0], self.config[result[0]]['ip']))
        self.storage.close_session()

        for err in self.stat:
            logger.warning(err)


def worker(host_data):
    hostname = host_data[1]['name']
    host_ip = host_data[1]['ip']
    template_name = host_data[1]['template']
    plugin_path = host_data[0]
    logger.info('Start backup device - Hostname: {} IP: {}'.format(hostname, host_ip))
    plugin_base = PluginBase(package='ccnd.plugins')
    plugin_source = plugin_base.make_plugin_source(searchpath=[plugin_path])
    plugin_net_dev = plugin_source.load_plugin(template_name)
    template = plugin_net_dev.setup()
    template.load_data(host_data[1])
    result = template.activate()
    if result == 'ERR':
        logger.info('Error backup device - Hostname: {} IP: {}'.format(hostname, host_ip))
        return hostname, result
    template.deactivate()
    logger.info('End backup device - Hostname: {} IP: {}'.format(hostname, host_ip))
    return hostname, result


def logs():
    log_file = str(os.path.dirname(os.path.abspath(__file__))) + '/backup.log'
    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
    logging.basicConfig(format=u'%(asctime)s %(levelname)s %(name)s: %(message)s',
                        level=logging.INFO, handlers=[handler])

    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl


def main():
    logs()
    cli = CliManager()
    bm = BackupManager(cli.get_params())
    bm.run()
    # print(a.__dict__)
    # for i in a.config.values():
    #     print(i)
    # dl = a.template_source.load_plugin('dlink')
    # pool = Pool(processes=4)
    # results = pool.map(func=worker, iterable=a.config.values())
    # pool.close()
    # pool.join()
    # print(list(a.config.values())[0])
    # result = worker(list(a.config.values())[0])

    # print(results)
    # print(a.__dict__)


if __name__ == '__main__':
    main()
