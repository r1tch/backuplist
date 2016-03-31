#!/usr/bin/env python3

import csv
import dvdmetadata
import time
import traceback

from fileutil import FileUtil

class BackupFile:
    """A file already stored on DVD"""

    def __init__(self, fullpath="", relpath="", dvdmetadata=None):
        self.relpath = relpath
        self.dvdmetadata = dvdmetadata
        if fullpath:
            try:
                self.timestamp = FileUtil.TimeChanged(fullpath)
                self.size = FileUtil.SizeInBytes(fullpath)
                self.md5sum = FileUtil.ComputeMd5sum(fullpath)
            except KeyboardInterrupt as e:
                raise e
            except:
                self.relpath = ""
                print(traceback.format_exc())

    def isValid(self):
        return self.relpath != ""

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.md5sum)

    def write(self, csv_string):
        """To be used for creating CSV encoding of self"""
        self.csv_string = csv_string

    def __str__(self):
        return "{} ({} - {})".format(self.relpath, self.dvdmetadata.label, self.dvdmetadata.timestamp)

    def fromCsv(self, csvString):
        # note: loop should run once:
        for row in csv.reader([csvString]):
            if len(row) != 6:
                print("Invalid CSV line: " + csvString)
                return
            self.dvdmetadata = dvdmetadata.DvdMetadata(row[0], row[1])
            self.relpath = row[2]
            self.size = int(row[3])
            self.md5sum = row[4]
            self.timestamp = float(row[5])

    def __repr__(self):
        fileobj = self
        writer = csv.writer(fileobj)
        writer.writerow([self.dvdmetadata.label, self.dvdmetadata.timestamp, self.relpath, self.size, self.md5sum, self.timestamp])

        return self.csv_string


