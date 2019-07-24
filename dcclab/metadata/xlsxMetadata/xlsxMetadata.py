import xlrd
import os
import re

class XLSXMetadata:
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

    def getKeys(self) -> dict:
        keys = {}
        try:
            for worksheet in self.worksheets:
                header = {}
                for col in range(worksheet.ncols):
                    key = str(worksheet.cell_value(0, col)).replace('(HZ)', '')
                    key = re.sub('^\\s{1,99}', '', key)
                    key = re.sub('$\\s{1,99}', '', key)
                    key = re.sub('\\s', '_', key)
                    header[key] = 'TEXT'
                keys[worksheet.name] = header
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
                for col in range(worksheet.ncols):
                    key = str(worksheet.cell_value(0, col)).replace('(HZ)', '')
                    key = re.sub('^\\s{1,99}', '', key)
                    key = re.sub('$\\s{1,99}', '', key)
                    key = re.sub('\\s', '_', key)
                    cols[key] = str(worksheet.cell_value(row, col)).replace(',', '')
                sheet[row] = cols
            dictio[worksheet.name] = sheet

        return dictio
