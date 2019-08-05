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
                    dictio[key] = value
            except:
                pass
        return dictio

    @property
    def keys(self):
        return {'ZebrafishRAW': {'no.of.channels': 'INTEGER', 'frame.count': 'INTEGER', 'x.pixels': 'INTEGER',
                                 'y.pixels': 'INTEGER', 'x.voltage': 'REAL', 'y.voltage': 'REAL',
                                 'pixel.resolution': 'REAL', 'Laser.Power': 'REAL'}}
