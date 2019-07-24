from dcclab import findFiles
from dcclab import Metadata
from dcclab import Database
import xlrd
import re
import os


# Read the xlsx file.
# -> From xlsx line, create xlsxMetadata object.
# -> Get primary metadata from the xlsx line.
# Opt. ? -> Analyse file path in the xlsx line. (.raw file)
# Opt. ? -> Find the .ini file related to the .raw file path.
# Opt. ? -> -> Find more metadata from the .ini file if relevant.
# -> Export as a dict.
# -> Add dict to database.

# What database? Where?
# Cafeine2 is a server and pdk has a whole different server so where should the database go?


def createPDKDatabase():
    # Current directory is :
    print('Beginning process...')
    directory = os.path.dirname(__file__)
    print('Directory is : {}'.format(directory))

    # Path to the Paul de Koninck's database is :
    pdkPath = os.path.join(directory, 'dcclab', 'database', 'pdk.db')
    print('Path to database "pdk.db" is : {}'.format(pdkPath))
    print('Connecting to database...')

    # We create a database object in rwc mode. If the database doesn't exist, we create it.
    # Then we connect to the database.
    # Database is in asynchronous mode for faster inserts.
    with Database(pdkPath, True) as database:
        print('Dropping all existing tables if any...')
        database.dropTable('xlsxMetadata')
        database.commit()
        print('Done.')

        print("WARNING : Database is in asynchronous mode.")
        database.asynchronous()

        # Now, we need paths to our metadata (the .raw files and the .xlsx file.)
        # For the .xlsx, we have :
        xlsxPath = os.path.join(directory, 'dcclab', 'PDK', 'Calcium_imaging_file_info.xlsx')
        print('Path to file data is : {}'.format(xlsxPath))

        # For the .raw, we have :
        print('Finding raw files in PDK...')
        files = findFiles(os.path.join(directory, 'dcclab', 'PDK'), 'raw')
        print('{} raw files were found!'.format(len(files)))

        # Now, we extract the metadata from our files. First, we start with the .csv files.
        # We extract the metadata.
        print('Extracting metadata from .xlsx file...')
        xlsxMetadata = Metadata(xlsxPath)
        print('...Done!')

        # We create tables for the metadata.
        print('Creating tables for the .xlsx metadata...')
        database.beginTransaction()
        database.createTable(xlsxMetadata.keys)
        database.commit()
        print('...Done!')

        # We insert the .xlsx Metadata into the tables.
        print('Inserting metadata into the database...')
        entries = xlsxMetadata.metadata
        database.beginTransaction()
        for sheet in entries.values():
            for row in sheet.values():
                database.insert('xlsxMetadata', row)
        database.commit()
        print('xlsxMetadata was processed for {} lines...'.format(len(entries)))

        # Skip the raw files for now.  # TODO

    print('Database was successfully created.')


if __name__ == '__main__':
    createPDKDatabase()

    # Reading the xlsx file
    '''
    xlsx = 'K:\\Calcium_imaging_file_info.xlsx'
    mtdt = Metadata(xlsx)

    for sheet in mtdt.metadata.values():
        for row in sheet.values():
            print(row)
    '''

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
