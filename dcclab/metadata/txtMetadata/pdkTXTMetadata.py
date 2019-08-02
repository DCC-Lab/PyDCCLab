class PDKTXTMetadata:
    def __init__(self, path):
        self.path = path
        self.dict = self.getDictFromFile()

    def readFile(self):
        with open(self.path, 'r') as file:
            lines = file.readlines()
        return lines

    def getDictFromFile(self):
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

    def getKeys(self):
        return {'no.of.channels': 'INTEGER', 'frame.count': 'INTEGER', 'x.pixels': 'INTEGER', 'y.pixels': 'INTEGER',
                'x.voltage': 'REAL', 'y.voltage': 'REAL', 'pixel.resolution': 'REAL', 'Laser.Power': 'REAL'}
