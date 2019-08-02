import xml.etree.ElementTree as et
from ..txtMetadata.pdkTXTMetadata import PDKTXTMetadata
import re
import os
import datetime


class PDKRAWMetadata:
    def __init__(self, rawPath):
        self.rawPath = rawPath
        self.fileName = self.__fileName()
        self.date = self.__date()

        # Processing .ini file :
        self.iniDict, self.iniKeys = self.extractDataFromIniFile()

        # Processing .xml file :
        self.xmlPath = self.__xmlPath()
        self.xmlRoot = self.readXmlFile()

    def __fileName(self):
        file = os.path.basename(self.rawPath)
        return os.path.splitext(file)[0]

    def __date(self):
        fileName = self.fileName.split('_')[0:4]
        fileName = str.join('_', fileName)
        date = datetime.datetime.strptime(fileName, '%Y%m%d_%H_%M_%S')
        return '{} {}'.format(date.date(), date.time())

    def extractDataFromIniFile(self):
        mtdt = PDKTXTMetadata(self.rawPath)
        return mtdt.asDict, mtdt.keys

    # FixMe Currently, we do not know if .xml files associated with .raw files have any valuable metadata.
    def __xmlPath(self):
        return re.sub('XYT\.lineshifted\.raw|XYT.raw', 'OME.xml', self.rawPath, re.IGNORECASE)

    # FixMe Currently, we do not know if .xml files associated with .raw files have any valuable metadata.
    def readXmlFile(self):
        tree = et.parse(self.xmlPath)
        return tree.getroot()

    @property
    def keys(self):
        keys = {'path': 'TEXT PRIMARY KEY'}
        return {**keys, **self.iniKeys}

    @property
    def asDict(self):
        dictio = {'path': self.rawPath}
        return {**dictio, **self.iniDict}
