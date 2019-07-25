import xml.etree.ElementTree as et
import re
import os
import datetime


class RAWMetadata:
    def __init__(self, rawPath):
        self.rawPath = rawPath
        # Data from file name.
        self.fileName = self.__fileName()
        self.date = self.__date()

        # Getting secondary files for metadata.
        self.iniPath = self.__iniPath()
        self.xmlPath = self.__xmlPath()  # FixMe This might not be necessary. Delete if xml are irrelevant.

        # Data from secondary files.
        self.iniLines = self.readIniFile()
        self.xmlRoot = self.readXmlFile()  # FixMe This might not be necessary. Delete if xml are irrelevant.

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

    def __xmlPath(self):  # FixMe This might not be necessary. Delete if xml are irrelevant.
        return re.sub('XYT\.lineshifted\.raw|XYT.raw', 'OME.xml', self.rawPath, re.IGNORECASE)

    def readIniFile(self):  # TODO What's important in the .ini file? Is there anything important?
        with open(self.iniPath, 'r') as file:
            lines = file.readlines()
        return lines

    def extractDataFromIniFile(self):
        keys = ['no.of.channels', 'frame.count', 'x.pixels', 'y.pixels', 'x.voltage', 'y.voltage', 'pixel.resolution',
                'Laser.Power']
        iniLines = self.readIniFile()
        for line in iniLines:
            key, value = line.split(' = ')

    def readXmlFile(self):
        tree = et.parse(self.xmlPath)
        return tree.getroot()
