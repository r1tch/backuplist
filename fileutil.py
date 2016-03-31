#!/usr/bin/env python3

import hashlib
import os

class FileUtil:
    def TimeChanged(filename):
        return os.path.getmtime(filename)

    def SizeInBytes(filename):
        return os.path.getsize(filename)

    def ComputeMd5sum(filename):
        # from http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
