#!/usr/bin/env python3

import os

class FileProp:
    """File properties to quickly identify files"""
    def __init__(self, backupfile):
        self.basename = os.path.basename(backupfile.relpath)
        self.size = backupfile.size
        self.timestamp = int(backupfile.timestamp)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.basename, self.size, self.timestamp))

    def __str__(self):
        return "{} ({} {})".format(self.basename, self.size, self.timestamp)

