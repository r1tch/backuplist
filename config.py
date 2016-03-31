#!/usr/bin/env python3

import configparser

config = Config()

class Config(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        local_dir = os.path.expanduser("~/.backuplist")
        try:
            os.mkdir(local_dir)
        except FileExistsError:
            pass

        self.set_default_values()
        self.read(local_dir + "/config.ini")

    def set_default_values(self):
        self.add_section("default")
        # self.set("logging", "level", str(logging.DEBUG))     # to be replaced by WARNING after prod release



