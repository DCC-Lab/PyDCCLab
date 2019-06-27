from dcclab import Database
import os


if __name__ == '__main__':
    directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    print(directory)
    path = os.path.join(directory, 'mountPom', 'injection AAV', 'résultats bruts', 'mtp.db')
    print(path)
    #database = Database(r'P:\injection AAV\résultats bruts\mtp.db')
    database = Database(path)
    database.connect()

    '''
    select = database.select('cziChannels', 'channel_id', 'channel_name="DAPI"')
    with open('query.csv', 'w', encoding='UTF-8') as file:
        for line in select:
            file.write('{}\n'.format(line['channel_id']))
    '''

    select = database.select('cziMetadata', 'path', 'channels<1')
    with open('query.csv', 'w', encoding='UTF-8') as file:
        for line in select:
            file.write('{}\n'.format(line['path']))