'''
This is a script used to create the mtp.db database.
This database contains metadata linked to Molecular Tools platform's operations.
'''
from dcclab import Database
from dcclab import Metadata
from dcclab import findFiles


if __name__ == '__main__':
    # TODO This whole script seems to take a while. The INSERT OR REPLACE in database.insert() seems to be the cause.
    # We need paths to our metadata
    # We get a list of paths to the czi files.
    print('Searching for czi files...')
    cziFiles = findFiles(r'P:\injection AAV\résultats bruts\AAV', '*.czi') + \
               findFiles(r'P:\injection AAV\résultats bruts\RABV', '*.czi')
    print('{} files were found!'.format(len(cziFiles)))

    # And paths to our csv files.
    # The csv files can be turned into metadata objects right away.
    miceCSV = r'C:\Users\MathieuLaptop\Documents\Ulaval\ProgPython\Projets\BigData-ImageAnalysis\dcclab\tests\Data-souris.csv'
    usesCSV = r'C:\Users\MathieuLaptop\Documents\Ulaval\ProgPython\Projets\BigData-ImageAnalysis\dcclab\tests\Data-Utilisation.csv'
    print('Processing csv metadata...')
    miceMetadata = Metadata(miceCSV)
    usesMetadata = Metadata(usesCSV)

    # We create the database in the desired directory.
    print('Connecting to database...')
    database = Database(r'P:\injection AAV\résultats bruts\mtp.db', 'rwc')
    database.connect()

    # We create the tablse for the csv Metadata.
    print('Processing csv metadata into the database...')
    database.createTable(miceMetadata.keys)
    database.commit()
    database.createTable(usesMetadata.keys)
    database.commit()

    # We insert the csv Metadata into the tables.
    entries = miceMetadata.metadata
    for line in entries.keys():
        database.insert('Data-souris', entries[line])
        database.commit()
    print('Data-souris was processed for {} lines...'.format(len(entries)))

    entries = usesMetadata.metadata
    for line in entries.keys():
        database.insert('Data-Utilisation', entries[line])
        database.commit()
    print('Data-Utilisation was processed for {} lines...'.format(len(entries)))

    # We now process the czi files into the database.
    # We create the tables.
    print('Processing czi files into the database...')
    cziMetadata = Metadata(cziFiles[0])
    database.createTable(cziMetadata.keys)
    print('Tables were created, processing the files...')

    for cziFile in cziFiles:
        print('Processing {}...'.format(cziFile))
        cziMetadata = Metadata(cziFile)
        database.insert('cziMetadata', cziMetadata.metadata)
        database.commit()
        for channelId in cziMetadata.channels.keys():
            database.insert('cziChannels', cziMetadata.channels[channelId])
            database.commit()
    print('{} czi files were processed!'.format(len(cziFiles)))
    database.disconnect()
    print('Done!')
