import re


class PDKTXTMetadata:
    def __init__(self, path):
        self.path = path
        self.iniPath = self.__iniPath()

    def __iniPath(self):
        return re.sub('\.lineshifted\.raw|.raw', '.ini', self.path, re.IGNORECASE)

    def readFile(self):
        with open(self.iniPath, 'r') as file:
            lines = file.readlines()
        return lines

    @property
    def asDict(self):
        keys = ['no.of.channels', 'frame.count', 'x.pixels', 'y.pixels', 'x.voltage', 'y.voltage', 'pixel.resolution',
                'Laser.Power']
        dictio = {}
        lines = self.readFile()
        for line in lines:
            try:
                line = line.split(' = ')
                key = line[0]
                value = line[1].rstrip('\n')
                if key in keys:
                    dictio[key.replace('.', '_')] = value
            except:
                pass
        return dictio

    @property
    def keys(self):
        return {'no_of_channels': 'INTEGER', 'frame_count': 'INTEGER', 'x_pixels': 'INTEGER', 'y_pixels': 'INTEGER',
                'x_voltage': 'REAL', 'y_voltage': 'REAL', 'pixel_resolution': 'REAL', 'Laser_Power': 'REAL'}
