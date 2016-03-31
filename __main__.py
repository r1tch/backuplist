#!/usr/bin/env python3

import sys

from database import Database

def printUsage():
    print("""Usage: 

{0} add <path to mounted dvd>
       - record files of a freshly burnt DVD in the database

{0} find <what>
       - find info about files in the database

{0} prep <path to files to backed up> <path to temp directory>
       - copies all files not yet backed up to temporary directory, retaining dir structure
""".format(sys.argv[0]))



if __name__ == '__main__':
    if len(sys.argv) < 3:
        printUsage()
        sys.exit(1)

    if sys.argv[1] == "add":
        db = Database()
        db.add(sys.argv[2])
        db.writeDatabase()
    elif sys.argv[1] == "find":
        searchString = sys.argv[2]
        db = Database(searchString)
    else:
        printUsage()

