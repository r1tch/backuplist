#!/usr/bin/env python3

import os
import sys
from shutil import copyfile, copystat

from backupfile import BackupFile
from dvdmetadata import DvdMetadata
from fileprop import FileProp


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
        self.backupFileDict = dict()
        self.backupFileByMd5 = dict()
        self.dvdset = set()

        if os.path.exists(Database.DbFile):
            print("Reading {}...".format(Database.DbFile))
            self.readDatabase(searchString)
            print("Done.")

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

    def prep(self, filePath, destPath):
        filePath = os.path.abspath(filePath)

        for parent, dirs, files in os.walk(filePath):
            for f in files:
                if f.startswith("."):
                    print("Ignoring hidden file:{}".format(f))
                    continue
                fullpath = os.path.join(parent, f)
                relpath = os.path.relpath(fullpath, filePath)
                do_md5_calc = False
                backupfile_nomd5 = BackupFile(fullpath, relpath, None,
                                              do_md5_calc)
                fileprop = FileProp(backupfile_nomd5)

                if fileprop.size > (4 * 1024 * 1024 * 1024 - 1):
                    print("Ignoring file >= 4G: {} (size:{})".format(
                        f, fileprop.size))
                    continue

                if fileprop in self.backupFileDict:
                    relpath = self.backupFileDict[fileprop].relpath
                    print("Already in DB: {}".format(relpath))
                elif not self._attemptToAlias(fullpath, relpath):
                    self._copyToTempDir(fullpath, relpath, destPath)

    def _attemptToAlias(self, fullpath, relpath):
        backupfile = BackupFile(fullpath, relpath)

        if backupfile.md5sum in self.backupFileByMd5:
            orig = self.backupFileByMd5[backupfile.md5sum][0]
            if orig.size == backupfile.size:
                backupfile.makeAliasOf(orig)
                print("Alias found: {} for: {}".format(backupfile, orig))
                self._addNewFile(backupfile)
                return True

        return False

    def _copyToTempDir(self, fullpath, relpath, destPath):
        target_dir = os.path.join(destPath, os.path.dirname(relpath))
        os.makedirs(target_dir, 0o777, exist_ok=True)

        target_file = os.path.join(destPath, relpath)
        if os.path.exists(target_file):
            source_backupfile = BackupFile(fullpath, relpath)
            dest_backupfile = BackupFile(target_file, relpath)
            if not source_backupfile.isSameAs(dest_backupfile):
                print("Different target already exists, please investigate")
                print("Source: {}\nTarget: {}".format(fullpath, target_file))
                sys.exit(1)
            print("Already copied: {}".format(target_file))
            return

        copyfile(fullpath, target_file)
        copystat(fullpath, target_file)
        print("{} -> {}".format(fullpath, target_dir))

    def _addNewFile(self, backupfile):
        if not backupfile:
            raise TypeError("Attempting to add NoneType to backupFileSet")

        if backupfile in self.backupFileSet:
            return

        self.backupFileList.append(backupfile)
        self.backupFileSet.add(backupfile)
        self.backupFileDict[FileProp(backupfile)] = backupfile
        if backupfile.md5sum in self.backupFileByMd5:
            self.backupFileByMd5[backupfile.md5sum].append(backupfile)
        else:
            self.backupFileByMd5[backupfile.md5sum] = [backupfile]

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
        print("Writing {}...".format(Database.DbFile))
        os.rename(Database.DbFile, Database.DbFile + ".bak")
        f = open(Database.DbFile, "w")
        for backupfile in self.backupFileList:
            f.write(backupfile.__repr__())
        print("Done.")
