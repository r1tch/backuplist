# Backuplist

## Introduction

Aim of backuplist is to track data that has been backed up onto WORM
(write-once-read-many) media, eg, DVDs, BluRays, etc.

With backuplist you can prepare previously unsaved data from a collection
for burning. For example, if you have a huge photo collection, but every
now and then only a handful of images get altered / added: you definitely
would not want to re-backup the whole collection over again.

Backuplist will:
- detect new/modified files requiring backup, copy them to a specified location for burning
- read burned discs and add contents to the database
- find files in the database

## Build the Binary

...just use minipex. (TODO: more description about minipex...)

## Usage

### Step 1: Preparation

`backuplist prep <path to files to back up> <path to temp directory>`

Will search your collection and copy all files not found in the database to the
temporary directory.

This step will detect renamed/moved files (aliases, using timestamps, md5
hashes) and make a note of them, they will not be re-added.

### Step 2: Burn

Burn the contents of the temporary directory. It is advised to specify a
meaningful disk label and write this label on the disk itself, this will be
stored in the database and shown during searches. (Either use date/time or
something like PHOTOS01, PHOTOS02, etc.)

### Step 3: Add to Database

Insert the freshly burnt disk, and issue:

`backuplist add <path to mounted disk>`

This will read the disk label, read info about all files and add them to the database.

Re-reading the disk is useful as a verification step, to make sure the data is readable.

### Searching the Database

`backuplist find <what>`

For now, this only uses case-insensitive text search in the database.


### Reconstruction upon Data Loss

The directory structure is preserved, a simple copy from the disk should be enough, eg:

  `cp -R /mnt/mydvd/* /path/to/my/collection`


## Room for Improvement

- add burning capabilities with auto labeling (date-time)
- periodic automated preparation, sending email when a full disk worth is ready to be burnt
- GUI and multi-platform, Windows, Mac
- reconstruction of original directory structure

