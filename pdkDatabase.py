from dcclab import findFiles
import xlrd
import re


if __name__ == '__main__':
    # Reading the xlsx file
    xlsx = 'K:\\Calcium_imaging_file_info.xlsx'
    with xlrd.open_workbook(xlsx) as file:
        sheet = file.sheet_by_index(0)

        for row in range(sheet.nrows):
            line = ''
            for col in range(sheet.ncols):
                line += '{}|'.format(sheet.cell_value(row, col))
            line = line.replace(' ', '')
            print(line.rstrip('|'))

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
