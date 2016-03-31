#!/usr/bin/env python3

import os

from backupfile import BackupFile
from dvdmetadata import DvdMetadata

class Database:

    DbFile = os.path.expanduser("~/.backuplist/database.csv")

    def __init__(self, searchString=""):
        local_dir = os.path.expanduser("~/.backuplist")
        try:
            os.mkdir(local_dir)
        except FileExistsError:
            pass

        self.backupFileList = []
        self.backupFileSet = set()
        self.dvdset = set()
        
        if os.path.exists(Database.DbFile):
            self.readDatabase(searchString)


    def add(self, dvd_path):
        dvd_path = os.path.abspath(dvd_path)

        dvd = DvdMetadata()
        dvd.readDisk()

        for parent, dirs, files in os.walk(dvd_path):
            for f in files:
                fullpath = os.path.join(parent, f)
                relpath = os.path.relpath(fullpath, dvd_path)
                backupfile = BackupFile(fullpath, relpath, dvd)
                if backupfile.isValid():
                    self._addNewFile(backupfile)
                    print("... " + str(backupfile))
                else:
                    print("ERROR ADDING " + fullpath)

    def _addNewFile(self, backupfile):
        if backupfile in self.backupFileSet:
            return

        self.backupFileList.append(backupfile)
        self.backupFileSet.add(backupfile)
        self.dvdset.add(backupfile.dvdmetadata)

    def readDatabase(self, searchString):
        searchString = searchString.lower()
        with open(Database.DbFile) as f:
            for line in f:
                backupfile = BackupFile()
                backupfile.fromCsv(line)
                if backupfile.isValid():
                    if searchString:
                        if line.lower().find(searchString) != -1:
                            print(backupfile)
                    else:
                        self._addNewFile(backupfile)

    def writeDatabase(self):
        os.rename(Database.DbFile, Database.DbFile + ".bak")
        f = open(Database.DbFile, "w")
        for backupfile in self.backupFileList:
            f.write(backupfile.__repr__())

