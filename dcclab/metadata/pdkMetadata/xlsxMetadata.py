import xlrd
import os

class XLSXMetadata:
    # Dev notes : The file is a RAW movie type file.
    # The metadata is in a .ini file within the same folder as the .raw file.
    def __init__(self, xlsxPath):
        self.path = xlsxPath
        self.name = self.fileName()

        self.workbook = self.getWorkbook()
        self.worksheets = self.getWorksheets()
        self.keys = self.getKeys()

    def fileName(self):
        file = os.path.basename(self.path)
        return os.path.splitext(file)[0]

    def getWorkbook(self) -> xlrd.book:
        try:
            return xlrd.open_workbook(self.path)
        except:
            raise

    def getWorksheets(self):
        worksheets = []
        try:
            for sheet in range(self.workbook.nsheets):
                worksheets.append(self.workbook.sheet_by_index(sheet))
            return worksheets
        except:
            return worksheets

    def getKeys(self):
        keys = {}
        try:
            for sheet in self.worksheets:
                header = {}
                for col in range(sheet.ncols):
                    header[sheet.cell_value(0, col)] = 'TEXT'
                keys[sheet.name] = header
            return keys
        except:
            return keys

    @property
    def asDict(self) -> dict:
        dictio = {}
        for worksheet in self.worksheets:
            sheet = {}
            for row in range(1, worksheet.nrows):
                cols = {}
                for col in range(worksheet.ncolss):
                    cols[worksheet.cell_value(0, col)] = worksheet.cell_value(row, col)
                sheet[row] = cols
            dictio[worksheet.name] = sheet

        return dictio
