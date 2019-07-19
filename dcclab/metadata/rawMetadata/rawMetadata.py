import xml.etree.ElementTree as et
import re
import os
import datetime

class RAWMetadata:
    def __init__(self, rawPath):
        self.rawPath = rawPath
        self.fileName = self.__fileName()
        self.date = self.__date()

        self.iniPath = self.__iniPath()
        self.xmlPath = self.__xmlPath()  # FixMe This might not be necessary. Delete if xml are irrelevant.
        self.iniLines = self.readIniFile()
        self.xmlLines = self.readXmlFile()  # FixMe This might not be necessary. Delete if xml are irrelevant.

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
        return re.sub('\.lineshifted\.raw|.raw', '.xml', self.rawPath, re.IGNORECASE)

    def readIniFile(self):
        return ''

    def openIniFile(self):
        pass

    def readXmlFile(self):
        return ''

    def openXmlFile(self):
        pass