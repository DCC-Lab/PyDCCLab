import xml.etree.ElementTree as et
import re
import os

class RAWMetadata:
    def __init__(self, rawPath):
        self.rawPath = rawPath
        self.fileName = self.__fileName()


        self.iniPath = self.__iniPath()
        self.xmlPath = self.__xmlPath()  # FixMe This might not be necessary. Delete if xml are irrelevant.
        self.iniLines = self.readIniFile()
        self.xmlLines = self.readXmlFile()  # FixMe This might not be necessary. Delete if xml are irrelevant.

    def __fileName(self):
        file = os.path.basename(self.rawPath)
        return os.path.splitext(file)[0]

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