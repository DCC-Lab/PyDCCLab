import sqlite3 as lite
import urllib.parse as parse
import pathlib
import platform


class Database:
    def __init__(self, path, mode='ro'):
        # Possible modes are 'ro', 'rw', and 'rwc'. Default should be 'ro'.
        self.mode = mode
        self.__path = path
        self.connection = None
        self.cursor = None

    def __del__(self):
        self.disconnect()

    @property
    def path(self):  # TODO MacOS and Linux will have to be added eventually.
        path = pathlib.Path(self.__path)
        if platform.system() == 'Windows':
            return 'file:' + parse.quote(path.as_posix(), safe=':/') + '?mode=' + self.mode
        if platform.system() == 'Darwin':
            pass
        if platform.system() == 'Linux':
            pass
        if path.is_absolute():
            return path.as_uri() + '?mode=' + self.mode

    def connect(self):
        try:
            if not self.isConnected:
                self.connection = lite.connect(self.path, uri=True)
                self.connection.row_factory = lite.Row
                self.cursor = self.connection.cursor()
                return True
        except:
            return False

    def disconnect(self):
        if self.isConnected:
            self.commit()
            self.connection.close()
            self.connection = None
            self.cursor = None

    @property
    def isConnected(self):
        return self.connection is not None

    def modifyConnection(self, mode):
        if not self.isConnected:
            self.disconnect()
        self.mode = mode
        self.connect()

    def commit(self):
        if self.isConnected:
            self.connection.commit()

    def rollback(self):
        if self.isConnected:
            self.connection.rollback()

    def execute(self, statement) -> lite.Row:
        if self.isConnected:
            self.cursor.execute(statement)
            return self.cursor.fetchall()

    @property
    def tables(self) -> list:
        rows = self.execute("SELECT name FROM sqlite_master WHERE type='table'")
        results = list(map(lambda row: row['name'], rows))
        return results

    def select(self, table, columns='*', condition=None) -> lite.Row:
        if condition is None:
            rows = self.execute("SELECT {0} FROM {1}".format(columns, table))            
        else:
            rows = self.execute("SELECT {0} FROM {1} WHERE {2}".format(columns, table, condition))
        return rows

    def createTable(self, metadata: dict):
        if self.isConnected:
            for table, keys in metadata.items():
                statement = "CREATE TABLE IF NOT EXISTS {} (".format(table)
                attributes = []
                for key, keyType in keys.items():
                    attributes.append("{} {}".format(key, keyType))
                statement += ",".join(attributes) + ")"
                self.cursor.execute(statement)

    def dropTable(self, table: str):
        if self.isConnected:
            statement = "DROP TABLE IF EXISTS {}".format(table)
            self.cursor.execute(statement)

    def insert(self, table: str, values: dict):
        if self.isConnected:
            lstKeys = []
            lstValues = []
            for key in values.keys():
                lstKeys.append(str(key))
                lstValues.append('"' + str(values[key]) + '"')
            keys = ','.join(lstKeys)
            values = ','.join(lstValues)
            statement = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'.format(table, keys, values)
            self.cursor.execute(statement)


# TODO Below is stuff to do eventually.
'''
def CreateNewDatabase(self):
    try:
        self.connection.connect(self.path, 'rwc')
        self.disconnect()
    except lite.OperationalError as error:
        raise error


def FindATable(cursor, tableName):
    try:
        listTables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for name in listTables:
            FormatedName = name
            FormatedName = str(FormatedName).replace('(', '')
            FormatedName = FormatedName.replace("'", "")
            FormatedName = FormatedName.replace(')', '')
            FormatedName = FormatedName.replace(',', '')
            if FormatedName == tableName:
                return True
        return False
    except connect.lite.OperationalError:
        raise Exception("An unforseen error has occurred.")


def ListAllTables(cursor):
    try:
        listTables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        formatedNamesList = []
        for name in listTables:
            formatedName = name
            formatedName = str(formatedName).replace('(', '')
            formatedName = formatedName.replace("'", "")
            formatedName = formatedName.replace(')', '')
            formatedName = formatedName.replace(',', '')
            formatedNamesList.append(formatedName)
        return formatedNamesList
    except connect.lite.OperationalError:
        raise Exception("An unforseen error has occurred.")
'''

if __name__ == '__main__':
    # If we want to create new tables in our database we proceed as follow :
    # We start with creating a proper ImageMetadata object.
    #path = 'P:\\injection AAV\\résultats bruts\\AAV\\AAV498AAV455\\AAV498AAV455_S94\\AAV498-455_S94_C.czi'
    #metadata = imgMtdt(path)

    # We connect to a database.
    #dbPath = 'C:\\Users\\MathieuLaptop\\Documents\\Ulaval\\ProgPython\\Projets\\BigData-ImageAnalysis\\testData\\test.db'
    #testDB = obsolete(dbPath, 'rw')
    #testDB.connect()

    # Drop the old tables.
    '''
    testDB.dropTable('czimetadata')
    testDB.commit()
    testDB.dropTable('czichannel')
    testDB.commit()

    testDB.createTable(metadata.keys)
    testDB.commit()
    
    testDB.disconnect()
    '''
    # If we want to insert into the database, we proceed as follow :
    # We connect to a database.
    dbPath = 'C:\\Users\\MathieuLaptop\\Documents\\Ulaval\\ProgPython\\Projets\\BigData-ImageAnalysis\\testData\\test.db'
    testDB = Database(dbPath, 'rw')
    testDB.connect()

    # We find all of the files/metadata that we want to process.
    #directories = [r'P:\injection AAV\résultats bruts\AAV', r'P:\injection AAV\résultats bruts\RABV']
    #filesList = findFiles(directories[0], '*.czi') + findFiles(directories[1], '*.czi')

    # Smaller directories for faster tests
    #directories = [r'P:\injection AAV\résultats bruts\AAV\AAV2 retro janelia\AAV2retro_S45']
    #filesList = findFiles(directories[0], '*.czi')

    # We process it.
    '''
    for file in filesList:
        print('Processing : ', file)
        metadata = imgMtdt(file)
        testDB.insert('cziMetadata', metadata.metadata)
        testDB.commit()

        for channelid, channel in metadata.channels.items():
            testDB.insert('cziChannels', channel)
            testDB.commit()
    '''

    # Query test.
    rows = testDB.select('cziChannels', 'channel_id', "channel_name='mCher'")
    newRows = []
    for row in rows:
        newRows.append(row[0].split(';'))

    file = open('querry_mcher.csv', 'w', encoding='UTF-8')
    for row in newRows:
        line = '{},{}\n'.format(row[0], row[1].lstrip('Channel:'))
        file.write(line)