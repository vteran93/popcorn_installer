import os


class Icons(object):

    SYMLINK = '/usr/bin/popcorn-time'
    ICON_IMAGE = '/opt/popcorn/src/app/images/icon.png'

    def __init__(self, logger, status):
        self.logger = logger
        self._status = status

    def configure_icons(self, version):
        
        success = True
        message = ''
        if not os.path.isfile(self.SYMLINK):
            success = False
            message+= " Symlink does not exists "
            
        if not os.path.isfile(self.ICON_IMAGE):
            success = False
            message+= ", Icon image is not installed "
        
        if not self._status.is_installed:
            success = False
            message+= ", Installation Status is wrong "
        
        if success:
            self._write_desktop_entry(version)
        else:
            self.logger.warning(f"Configure icons failed {message}")
            

    def _write_desktop_entry(self, version):
        content = self.__get_desktop_entry_content(version)
        with open('/usr/share/applications/popcorntime.desktop', 'w') as f:
            f.write(content)
            f.close()

    def __get_desktop_entry_content(self, version):
        entry = "[Desktop Entry]\n"
        entry += f"Version = {version}\n"
        entry += "Type = Application\n"
        entry += "Terminal = false\n"
        entry += "Name = Popcorn Time\n"
        entry += f"Exec = {self.SYMLINK}\n"
        entry += f"Icon = {self.ICON_IMAGE}\n"
        entry += f"Categories = Application;\n"

        return entry
