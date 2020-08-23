# -*- coding: UTF-8 -*-
from icons import Icons
from status import Status
from installer import Installer
from downloader import Downloader

import logging


class Main(object):

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.status = Status()
        self._downloader = Downloader(logging, self.status)
        self._installer = Installer(logging, self.status)
        self._icons = Icons(logging, self.status)

    def execute(self):
        if self._downloader.is_downloaded():
            downloaded_file = self._downloader.downloaded_file

        if self._downloader.should_install:
            self._installer.install(downloaded_file)
            self._icons.configure_icons(self.status.get_version())


if __name__ == "__main__":
    m = Main()
    m.execute()
