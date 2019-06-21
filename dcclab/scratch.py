from dcclab import Database


if __name__ == '__main__':
    database = Database(r'P:\injection AAV\résultats bruts\mtp.db')
    database.connect()

    select = database.select('cziChannels', 'channel_name')
    with open('query.txt', 'w') as file:
        for line in select:
            file.write('{}\n'.format(line['channel_name']))