import re


class RAWMetadata:
    def __init__(self, rawPath):
        self.rawPath = rawPath
        self.iniPath = self.iniPath()
        self.xmlPath = self.xmlPath()  # FixMe This might not be necessary. Delete if xml are irrelevant.

        self.iniLines = self.readIni()
        self.xmlLines = self.readXml()

    def iniPath(self):
        return re.sub('\.lineshifted\.raw|.raw', '.ini', self.rawPath, re.IGNORECASE)

    def xmlPath(self):  # FixMe This might not be necessary. Delete if xml are irrelevant.
        return re.sub('\.lineshifted\.raw|.raw', '.xml', self.rawPath, re.IGNORECASE)
