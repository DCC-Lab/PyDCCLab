import os


class CSVMetadata:
    def __init__(self, path):
        self.path = path
        self.name = self.fileName()

        # This is a quick test to catch if the file is of a valid type BEFORE we try to process it.
        self.canReadFile()

    def canReadFile(self):
        try:
            with open(self.path, 'r') as file:
                file.readline()
        except:
            raise

    def fileName(self):
        file = os.path.basename(self.path)
        return os.path.splitext(file)[0]

    @property
    def header(self) -> list:
        with open(self.path, 'r') as file:
            return file.readlines()[:2]

    @property
    def body(self) -> list:
        with open(self.path, 'r') as file:
            return file.readlines()[2:]

    @property
    def keys(self) -> dict:
        csvHeader = self.header
        keys = csvHeader[0].rstrip('\n').split(',')
        types = csvHeader[1].rstrip('\n').split(',')

        csvHeaderAsDict = {}
        for key, type in zip(keys, types):
            csvHeaderAsDict[key] = type

        return {self.name: csvHeaderAsDict}

    @property
    def lines(self) -> list:
        csvLines = self.body

        formattedLines = []
        for line in csvLines:
            formattedLines.append(line.rstrip('\n').split(','))

        return formattedLines

    @property
    def asDict(self) -> dict:
        keys = self.header[0].rstrip('\n').split(',')
        dictio = {}
        iter = 0
        for line in self.lines:
            metadataAsDict = {}
            for key, value in zip(keys, line):
                metadataAsDict[key] = value
            dictio[iter] = metadataAsDict
            iter += 1
        return dictio
