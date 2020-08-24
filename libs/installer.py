import os
import stat
import zipfile


class Installer(object):

    PATH_TO_INSTALL = '/opt/popcorn'
    BINARY = 'Popcorn-Time'
    USR_BIN = '/usr/bin'

    def __init__(self, logger, status):
        self.logger = logger
        self._status = status

    def install(self, downloaded_file):
        try:
            self.logger.info("Uncompressing")
            with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
                zip_ref.extractall(self.PATH_TO_INSTALL)

            self.__create_symlink()

            self._status.set_installed(True)
            self._status.save_status()

        except Exception as identifier:
            self.logger.error(f"We got an exception trying to install {identifier}")
            return False
        return True

    def __create_symlink(self):
        origin_route = os.path.join(self.PATH_TO_INSTALL, self.BINARY)
        destination_route = os.path.join(self.USR_BIN, self.BINARY).lower()
        self.logger.info("Creating symlink to " + destination_route)
        if not os.path.isfile(destination_route.lower()):
            os.system(f"ln -s {origin_route} {destination_route}")
