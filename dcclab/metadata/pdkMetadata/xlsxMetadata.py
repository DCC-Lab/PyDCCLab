import xlrd
import os

class XLSXMetadata:
    # Dev notes : The file is a RAW movie type file.
    # The metadata is in a .ini file within the same folder as the .raw file.
    def __init__(self, xlsxPath):
        self.path = xlsxPath
        self.name = self.fileName()
        self.workbook = self.getWorkbook()

    def getWorkbook(self) -> xlrd.book:
        try:
            return xlrd.open_workbook(self.path)
        except:
            raise

    def worksheets(self):
        worksheets = []
        try:
            for sheet in range(self.workbook.nsheets):
                worksheets.append(self.workbook.sheet_by_index(sheet))
            return worksheets
        except:
            return worksheets

    def fileName(self):
        file = os.path.basename(self.path)
        return os.path.splitext(file)[0]

    def __repr__(self):
        return {'xlsxMetadata': {'acquisition_frequency': self.acquisitionFrequency,
                                'acquisition_type': self.acquisitionType, 'image_dimensions': self.imageDimensions,
                                'objective': self.objective, 'number_of_frames': self.numberOfFrames,
                                'simulation': self.simulation, 'note': self.notes, 'file_path': self.filePath}}
