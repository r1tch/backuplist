#!/usr/bin/env python3

import copy
import csv
import dvdmetadata
import time
import traceback

from fileutil import FileUtil

class BackupFile:
    """A file already stored on DVD"""

    def __init__(self, fullpath="", relpath="", dvdmetadata=None, do_md5_calc=True):
        self.relpath = relpath
        self.dvdmetadata = dvdmetadata
        self.alias_of = None
        if fullpath:
            try:
                self.timestamp = FileUtil.TimeChanged(fullpath)
                self.size = FileUtil.SizeInBytes(fullpath)
                if do_md5_calc:
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
        # format:
        # dvdlabel,dvdtimestamp,relpath,size,md5sum,file_timestamp,alias_of_relpath,alias_of_timestamp
        # note: loop should run once:
        for row in csv.reader([csvString]):
            if len(row) != 8:
                print("Invalid CSV line: " + csvString)
                return
            self.dvdmetadata = dvdmetadata.DvdMetadata(row[0], row[1])  # TODO do not create a new object...
            self.relpath = row[2]
            self.size = int(row[3])
            self.md5sum = row[4]
            self.timestamp = float(row[5])

            if row[6] and row[7]:
                self.alias_of = copy.copy(self)
                self.alias_of.relpath = row[6]
                self.alias_of.timestamp = row[7]

    def __repr__(self):
        fileobj = self
        writer = csv.writer(fileobj)
        if self.alias_of:
            writer.writerow([self.dvdmetadata.label, self.dvdmetadata.timestamp, self.relpath, self.size, self.md5sum, self.timestamp, self.alias_of.relpath, self.alias_of.timestamp])
        else:
            writer.writerow([self.dvdmetadata.label, self.dvdmetadata.timestamp, self.relpath, self.size, self.md5sum, self.timestamp, '', ''])

        return self.csv_string

    def makeAliasOf(self, backupfile):
        # timestamp and relpath can differ, all others copied
        self.dvdmetadata = backupfile.dvdmetadata
        self.size = backupfile.size
        self.md5sum = backupfile.md5sum
        self.alias_of = backupfile

    def isSameAs(self, other_backupfile):
        return self.size == other_backupfile.size and self.md5sum == other_backupfile.md5sum
