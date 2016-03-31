#!/usr/bin/env python3

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
        """Reads DVD data from DVD inserted into drive"""
        descriptor = self.readPrimaryVolumeDescriptor()
        self.label=descriptor[40:72].decode().strip()
        creationTimestampPos=72+2*8+32+4*3+8+4*4+34+128*4+37*3

        # format: YYYYMMDDHHMMSShhx  -- hh = hundredths of sec, usually 00, x is timezone as integer, this one is _not_ ASCII
        self.timestamp=descriptor[creationTimestampPos:creationTimestampPos+14].decode()
        print("Read disk: " + self.label + " (" + self.timestamp + ")")

    def readPrimaryVolumeDescriptor(self):
        with open(DvdMetadata.Device, "rb") as image:
            image.seek(32768)
            return image.read(2048)

if __name__ == '__main__':
    dvd = DvdMetadata()
    dvd.readDisk()

    print("DVD label: {}, id: {}".format(dvd.label, dvd.timestamp))

