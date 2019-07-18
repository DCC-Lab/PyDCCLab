from dcclab import findFiles
from dcclab import Metadata
from dcclab import Database
import xlrd
import re


# Read the xlsx file.
# -> From xlsx line, create xlsxMetadata object.
# -> Get primary metadata from the xlsx line.
# Opt. ? -> Analyse file path in the xlsx line. (.raw file)
# Opt. ? -> Find the .ini file related to the .raw file path.
# Opt. ? -> -> Find more metadata from the .ini file if relevant.
# -> Export as a dict.
# -> Add dict to database.


if __name__ == '__main__':
    # Reading the xlsx file
    xlsx = 'K:\\Calcium_imaging_file_info.xlsx'
    mtdt = Metadata(xlsx)

    for sheet in mtdt.metadata.values():
        for row in sheet.values():
            print(row)

    '''
    with xlrd.open_workbook(xlsx) as file:
        sheet = file.sheet_by_index(0)

        for row in range(1, sheet.nrows):
            line = []
            for col in range(sheet.ncols):
                line.append(sheet.cell_value(row, col))
    '''

    '''
    # Reading the ini files.
    directory = 'K:\\'
    rawFiles = findFiles(directory, 'raw')
    iniFiles = []

    for rawFile in rawFiles:
        iniFiles.append(re.sub('\.lineshifted\.raw|.raw', '.ini', rawFile, re.IGNORECASE))

    for iniFile in iniFiles:
        try:
            with open(iniFile, 'r') as file:
                print(file.readlines())
        except:
            print(">>>>{} file doesn't work.".format(iniFile))
    '''
