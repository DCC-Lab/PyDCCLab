from dcclab import findFiles
from dcclab import Metadata
from dcclab import Database
import os


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
        database.dropTable('Files info')
        database.dropTable('ZebraFishRAW')
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
                database.insert('Files info', row)
        database.commit()
        print('xlsxMetadata was processed for {} sheet(s)...'.format(len(entries)))

        # Skip the raw files for now.
        print('Creating tables for the .raw metadata...')
        rawMetadata = Metadata(files[0])
        database.beginTransaction()
        database.createTable(rawMetadata.keys)
        database.commit()
        print('...Done!')

        # We insert the .raw Metadata into the tables.
        print('Inserting metadata into the database...')
        database.beginTransaction()
        for file in files:
            print('Processing {}...'.format(file))
            rawMetadata = Metadata(file)
            database.insert('ZebraFishRAW', rawMetadata.metadata)
        database.commit()
        print('{} czi files were processed!'.format(len(files)))
    print('Database was successfully created.')


if __name__ == '__main__':
    createPDKDatabase()
    pass
