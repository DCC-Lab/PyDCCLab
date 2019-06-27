from dcclab import Database
from dcclab import findFiles
from dcclab import Metadata
import os


if __name__ == '__main__':
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, 'POM', 'injection AAV', 'résultats bruts', 'mtp.db')
    print('Finding czi files in POM...')
    files = findFiles(os.path.join(directory, 'POM', 'injection AAV', 'résultats bruts', 'AAV'), '*.czi') + \
            findFiles(os.path.join(directory, 'POM', 'injection AAV', 'résultats bruts', 'RABV'), '*.czi')
    print('{} files found!'.format(len(files)))

    database = Database(path)
    database.connect()

    database.begin()
    for file in files:
        print('Processing file : {}'.format(file))
        mtdt = Metadata(file)
        database.insert('cziMetadata', mtdt.metadata)

        for channelId in mtdt.channels.keys():
            database.insert('cziChannels', mtdt.channels[channelId])
    database.commit()

    print('{} files were processed!'.format(len(files)))
    print('Proceeding to the query : ')

    select = database.select('cziChannels', 'channel_id', 'channel_name="mCher"')
    with open('query_mCher.csv', 'w', encoding='UTF-8') as file:
        for line in select:
            file.write('{}\n'.format(line['channel_id']))

    '''
    select = database.select('cziMetadata', 'path', 'channels<1')
    with open('query.csv', 'w', encoding='UTF-8') as file:
        for line in select:
            file.write('{}\n'.format(line['path']))
    '''
