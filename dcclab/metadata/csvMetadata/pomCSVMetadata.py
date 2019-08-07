from dcclab import checkIfValidDataType
import os


class POMCSVMetadata:
    def __init__(self, path):
        self.path = path
        self.name = self.fileName()

        self.separator = self.findSeparator()
        self.body = self.__body()
        self.columns = self.__columns()
        self.types = self.__types()

    def fileName(self):
        file = os.path.basename(self.path)
        return os.path.splitext(file)[0]

    def findSeparator(self):
        separator = None
        try:
            with open(self.path, 'r') as file:
                line = file.readline()

                if len(line.split(',')) >= 2:
                    separator = ','
                elif len(line.split(';')) >= 2:
                    separator = ';'
        except:
            raise
        return separator

    def __body(self) -> list:
        with open(self.path, 'r') as file:
            return file.readlines()

    def __columns(self) -> list:
        columns = str(self.body[0]).rstrip('\n').split(self.separator)
        self.body = self.body[1:]
        return columns

    def __types(self) -> list:
        removeLine = True
        types = str(self.body[0]).rstrip('\n').split(self.separator)
        iter = 0
        while iter < len(types):
            if not checkIfValidDataType(types[iter]):
                removeLine = False
                if self.columns[iter] == 'path':
                    types[iter] = 'TEXT PRIMARY KEY'
                else:
                    types[iter] = 'TEXT'
            iter += 1

        if removeLine:
            self.body = self.body[1:]

        return types

    @property
    def keys(self) -> dict:
        columns = self.columns
        types = self.types

        keys = {}
        for column, type in zip(columns, types):
            keys[column] = type

        return {self.name: keys}

    @property
    def lines(self) -> list:
        lines = self.body

        formattedLines = []
        for line in lines:
            formattedLines.append(line.rstrip('\n').split(self.separator))

        return formattedLines

    @property
    def asDict(self) -> dict:
        columns = self.columns
        dictio = {}
        iter = 0
        for line in self.lines:
            metadataAsDict = {}
            for column, value in zip(columns, line):
                metadataAsDict[column] = value
            dictio[iter] = metadataAsDict
            iter += 1
        return dictio
