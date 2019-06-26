class CSVMetadata:
    def __init__(self, path, name=None):
        self.path = path
        self.name = name

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

        return csvHeaderAsDict

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
