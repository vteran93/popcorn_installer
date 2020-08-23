
import re
import os
import json


class Status(object):
    STATUS_FILE = 'status.json'

    def __init__(self):
        pass

    def get_should_install(self):
        if os.path.isfile(self.STATUS_FILE):
            with open(self.STATUS_FILE, 'r') as status_manager:
                status = json.load(status_manager)['status']
                return status['should_install']
        return False

    def get_should_download(self, url_path):
        if os.path.isfile(self.STATUS_FILE):
            with open(self.STATUS_FILE, 'r') as status_manager:
                status = json.load(status_manager)['status']
                return status['version'] != self.__get_version_from_path(url_path)
        return True

    def get_version(self):
        if os.path.isfile(self.STATUS_FILE):
            with open(self.STATUS_FILE, 'r') as status_manager:
                status = json.load(status_manager)['status']
                return status['version']

    def save_status(self, download_version):
        with open(self.STATUS_FILE, 'w') as status_manager:
            json.dump({
                'status': {
                    'version':
                    self.__get_version_from_path(download_version),
                    'should_install': True
                }
            },
                status_manager)

    def __get_version_from_path(self, path):
        url_parts = os.path.split(path)
        search = re.search('\d+.\d+\.\d+', url_parts[1])
        if search:
            return search.group()
        raise Exception('Imposible to find version on path string')
