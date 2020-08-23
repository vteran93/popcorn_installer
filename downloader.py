# -*- coding: UTF-8 -*-
import re
import os
import requests
from clint.textui import progress

import bs4


class Downloader(object):

    CHUNK_SIZE = 1024
    LINUX_RESOURCE = 'https://popcorntime.app/linux'
    __downloaded_file = ''

    def __init__(self, logger, status):
        self.logger = logger
        self._status = status 

    def is_downloaded(self):
        url_path = self._get_path()
        local_name = self.__get_local_name(url_path)
        if self._should_download(url_path):
            self.logger.info("We are going to download...")
            self._download(url_path)
            self._status.save_status(self.__downloaded_file)
            return True

        if os.path.isfile(local_name):
            self.__downloaded_file = local_name
            return True

        return False

    @property
    def should_install(self):
        return self._status.get_should_install()

    @property
    def downloaded_file(self):
        return self.__downloaded_file

    @property
    def should_install(self):
        return self._status.get_should_install()

    def _get_path(self):
        self.logger.info("Getting download path...")

        linux_downloads_res = requests.get(self.LINUX_RESOURCE)
        linux_downloads_res.raise_for_status()
        soup = bs4.BeautifulSoup(linux_downloads_res.text, 'html.parser')

        url_link = soup.select('a[data-os="Linux"]')[1]

        self.logger.info("Getting version...")
        return url_link.get('href').strip()

    def _should_download(self, url_path):
        return self._status.get_should_download(url_path)
   
    def _download(self, url_path):
        self.logger.info("Downloading, sending request...")
        local_filename = self.__get_local_name(url_path)
        r = requests.get(url_path, allow_redirects=True)
        with open(local_filename, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in self.__progress_bar(total_length, r):
                f.write(chunk)
        self.__downloaded_file = local_filename

    def __progress_bar(self, total_length, reader):
        return progress.bar(reader.iter_content(chunk_size=self.CHUNK_SIZE),
                            expected_size=(total_length/self.CHUNK_SIZE) + 1)

    def __get_local_name(self, path):
        url_parts = os.path.split(path)
        return url_parts[1]

    