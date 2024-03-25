#!/usr/bin/env python3

import datetime
import os
import re
import subprocess
import sys

# note, info from:
# - http://alumnus.caltech.edu/~pje/iso9660.html 
# - http://www.commandlinefu.com/commands/view/12178/get-volume-id-label-of-iso9660-cd-rom
#
# While a disk might have more primary vol descriptor, but we assume to handle single-burnt full DVDs here
# No UUID is associated, so we'll just go with the date of creation

class DvdMetadata:
    """DVD disk metadata"""

    Device="/dev/cdrom"

    def __init__(self, label="", timestamp=""):
        self.label=label
        self.timestamp=timestamp

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.timestamp)

    def readDisk(self):
        if sys.platform == "linux" or sys.platform == "linux2":
            self.readDiskLinux()
        elif sys.platform == "darwin":
            self.readDiskMac()
        else:
            print("OS {} not handled".format(sys.platform))

        print("Read disk: " + self.label + " (" + self.timestamp + ")")

    def readDiskLinux(self):
        """Reads DVD data from DVD inserted into drive"""
        descriptor = self.readPrimaryVolumeDescriptorLinux()
        self.label=descriptor[40:72].decode().strip()
        creationTimestampPos=72+2*8+32+4*3+8+4*4+34+128*4+37*3

        # format: YYYYMMDDHHMMSShhx  -- hh = hundredths of sec, usually 00, x is timezone as integer, this one is _not_ ASCII
        self.timestamp=descriptor[creationTimestampPos:creationTimestampPos+14].decode()

    def readDiskMac(self):
        self.label = self.readLabelMac()
        tsunix = os.stat(os.path.join("/Volumes", self.label)).st_mtime
        print("ts unix of {}: {}".format(os.path.join("/Volumes", self.label), tsunix))
        tsdatetime = datetime.datetime.fromtimestamp(tsunix)
        self.timestamp = tsdatetime.strftime('%Y%m%d%H%M%S')

    def readPrimaryVolumeDescriptorLinux(self):
        with open(DvdMetadata.Device, "rb") as image:
            image.seek(32768)
            return image.read(2048)

    def readLabelMac(self):
        # List all disks and volumes
        process = subprocess.Popen(['diskutil', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        if err:
            raise Exception( "Error accessing disk utility.")

        # Decode output
        output = out.decode('utf-8')

        # Find the optical media device identifier
        optical_media_device = re.search(r'/dev/disk\d+ \(external, physical\):', output)
        if not optical_media_device:
            raise Exception( "No optical media found.")

        device_identifier = optical_media_device.group().split()[0]

        # Get information about the optical media
        process_info = subprocess.Popen(['diskutil', 'info', device_identifier], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_info, err_info = process_info.communicate()

        if err_info:
            raise Exception( "Error getting information about the optical media.")

        # Decode output
        output_info = out_info.decode('utf-8')

        # Find the Volume Name
        volume_name_match = re.search(r'Volume Name: +(.+)', output_info)
        if volume_name_match:
            return volume_name_match.group(1).strip()

        raise Exception( "Volume name not found.")


if __name__ == '__main__':
    dvd = DvdMetadata()
    dvd.readDisk()

    print("DVD label: {}, id: {}".format(dvd.label, dvd.timestamp))

