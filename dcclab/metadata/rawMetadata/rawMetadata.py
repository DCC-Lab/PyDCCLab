import xml.etree.ElementTree as et
import re
import os
import datetime


class RAWMetadata:
    # FixMe The PDK .raw files are weird to deal with. Their metadata is contained in others files, .ini and .xml,
    #  that are in the same folder as the .raw file. However, we do not know yet if these files have valuable data.
    #  Also, the .xml file seems rather poor in useful information. For now, the best thing to do is to deal with the
    #  .xlsx files contained in PDK. The functions to read and extract metadata from .ini and .xml files are
    #  placeholders, just in case.
    def __init__(self, rawPath):
        self.rawPath = rawPath
        # Data from file name.
        self.fileName = self.__fileName()
        self.date = self.__date()

        # Getting secondary files for metadata.
        self.iniPath = self.__iniPath()
        self.xmlPath = self.__xmlPath()

        # Data from secondary files.
        self.iniDict = self.extractDataFromIniFile()
        self.xmlRoot = self.readXmlFile()

    def __fileName(self):
        file = os.path.basename(self.rawPath)
        return os.path.splitext(file)[0]

    def __date(self):
        fileName = self.fileName.split('_')[0:4]
        fileName = str.join('_', fileName)
        date = datetime.datetime.strptime(fileName, '%Y%m%d_%H_%M_%S')
        return '{} {}'.format(date.date(), date.time())

    def __iniPath(self):
        return re.sub('\.lineshifted\.raw|.raw', '.ini', self.rawPath, re.IGNORECASE)

    def __xmlPath(self):
        return re.sub('XYT\.lineshifted\.raw|XYT.raw', 'OME.xml', self.rawPath, re.IGNORECASE)

    def readIniFile(self):
        with open(self.iniPath, 'r') as file:
            lines = file.readlines()
        return lines

    def extractDataFromIniFile(self):
        keys = ['no.of.channels', 'frame.count', 'x.pixels', 'y.pixels', 'x.voltage', 'y.voltage', 'pixel.resolution',
                'Laser.Power']
        iniDict = {}
        iniLines = self.readIniFile()
        for line in iniLines:
            try:
                line = line.split(' = ')
                key = line[0]
                value = line[1].rstrip('\n')
                if key in keys:
                    iniDict[key] = value
            except:
                pass
        return iniDict

    def getIniKeys(self):
        return {'no.of.channels': 'INTEGER', 'frame.count': 'INTEGER', 'x.pixels': 'INTEGER', 'y.pixels': 'INTEGER',
                'x.voltage': 'REAL', 'y.voltage': 'REAL', 'pixel.resolution': 'REAL', 'Laser.Power': 'REAL'}

    def readXmlFile(self):
        tree = et.parse(self.xmlPath)
        return tree.getroot()
