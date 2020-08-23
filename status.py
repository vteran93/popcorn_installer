
import re
import os
import json


class Status(object):
    STATUS_FILE = 'status.json'

    def __init__(self):
        pass

    def load_status(self):
        if os.path.isfile(self.STATUS_FILE):
            with open(self.STATUS_FILE, 'r') as status_manager:
                self._status = json.load(status_manager)['status']
            status_manager.close()

    def get_should_install(self):
        return self._status['should_install']
        
    def get_should_download(self, url_path):
        return self.get_version() != self.__get_version_from_path(url_path)
        
    def get_version(self):
        return self._status['version']

    def set_version(self, version):
        self._status['version'] = self.__get_version_from_path(version)

    def set_should_install(self, should_install):
        self._status['should_install'] = should_install
    
    def set_installed(self, installed):
        self._status['installed'] = installed

    @property
    def is_installed(self):
        return self._status['installed']

    def save_status(self):
        with open(self.STATUS_FILE, 'w') as status_manager:
            json.dump({
                'status': self._status
            },
                status_manager)
            status_manager.close()

    def __get_version_from_path(self, path):
        url_parts = os.path.split(path)
        search = re.search('\d+.\d+\.\d+', url_parts[1])
        if search:
            return search.group()
        raise Exception('Imposible to find version on path string')
