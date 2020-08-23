import os


class Icons(object):

    SYMLINK = '/usr/bin/popcorn-time'
    ICON_IMAGE = '/opt/popcorn-time/src/app/images/icon.png'

    def __init__(self, logger, status):
        self.logger = logger
        self._status = status

    def configure_icons(self, version):
        if os.path.isfile(self.SYMLINK) and\
                os.path.isfile(self.ICON_IMAGE) and\
                self._status.is_installed:

            self._write_desktop_entry(version)

    def _write_desktop_entry(self, version):
        content = self.__get_desktop_entry_content(version)
        with open('/usr/share/applications/popcorntime.desktop', 'w') as f:
            f.write(content)

    def __get_desktop_entry_content(self, version):
        return f"""
        [Desktop Entry]
        Version = {version}
        Type = Application
        Terminal = false
        Name = Popcorn Time
        Exec = {self.SYMLINK}
        Icon = {self.ICON}
        Categories = Application;
        """
