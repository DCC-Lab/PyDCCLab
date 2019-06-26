import sqlite3 as lite
import urllib.parse as parse
import pathlib


class Database:
    def __init__(self, path, mode='ro'):
        # Possible modes are 'ro', 'rw', and 'rwc'. Default should be 'ro'.
        self.__mode = mode
        self.__path = path
        self.__connection = None
        self.cursor = None

    def __del__(self):
        self.disconnect()

    @property
    def path(self):
        path = pathlib.Path(self.__path)
        return 'file:{}?mode={}'.format(parse.quote(path.as_posix(), safe=':/'), self.mode)

    @property
    def mode(self):
        return self.__mode

    def connect(self):
        try:
            if not self.isConnected:
                self.__connection = lite.connect(self.path, uri=True, isolation_level=None)
                self.__connection.row_factory = lite.Row
                self.cursor = self.__connection.cursor()
                return True
        except:
            return False

    def disconnect(self):
        if self.isConnected:
            self.commit()
            self.__connection.close()
            self.__connection = None
            self.cursor = None

    @property
    def isConnected(self):
        return self.__connection is not None

    def changeConnectionMode(self, mode):
        if self.isConnected:
            self.disconnect()
        self.__mode = mode
        self.connect()

    def commit(self):
        if self.isConnected:
            self.__connection.commit()

    def rollback(self):
        if self.isConnected:
            self.__connection.rollback()

    def execute(self, statement):
        if self.isConnected:
            self.cursor.execute(statement)

    def fetchAll(self):
        if self.isConnected:
            return self.cursor.fetchall()

    def fetchOne(self):
        if self.isConnected:
            return self.cursor.fetchone()

    @property
    def tables(self) -> list:
        self.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = self.fetchAll()
        results = list(map(lambda row: row['name'], rows))
        return results

    def select(self, table, columns='*', condition=None) -> lite.Row:
        if condition is None:
            self.execute("SELECT {0} FROM {1}".format(columns, table))
            rows = self.fetchAll()
        else:
            self.execute("SELECT {0} FROM {1} WHERE {2}".format(columns, table, condition))
            rows = self.fetchAll()
        return rows

    def createTable(self, metadata: dict):
        if self.isConnected:
            for table, keys in metadata.items():
                statement = 'CREATE TABLE IF NOT EXISTS "{}" ('.format(table)
                attributes = []
                for key, keyType in keys.items():
                    attributes.append('{} {}'.format(key, keyType))
                statement += ",".join(attributes) + ")"
                self.execute(statement)

    def dropTable(self, table: str):
        if self.isConnected:
            statement = "DROP TABLE IF EXISTS {}".format(table)
            self.execute(statement)

    def insert(self, table: str, values: dict):
        if self.isConnected:
            lstKeys = []
            lstValues = []
            for key in values.keys():
                lstKeys.append('"{}"'.format(str(key)))
                lstValues.append('"{}"'.format(str(values[key])))
            keys = ','.join(lstKeys)
            values = ','.join(lstValues)
            statement = 'INSERT OR REPLACE INTO "{}" ({}) VALUES ({})'.format(table, keys, values)
            self.execute(statement)

    # WARNING : Asynchronus mode means the database doesn't wait for something to be entirely written before it begins
    # to write something else. It has the potential of corrupting entries if the database crashed or there is a power
    # failure. However, asynchronus mode is much faster.
    def asynchronous(self):
        if self.isConnected:
            self.execute('PRAGMA synchronous = OFF')

    # With isolation_level = None for our connection, we disable the python auto-handling of BEGIN, etc. We reset to the
    # default SQLite handling. By default, SQLite is in auto-commit mode. It means that for each command, SQLite starts,
    # processes, and commits the transaction automatically. By issuing a BEGIN, we override this and manually handle
    # transactions. This allows faster writing on the database.
    def begin(self):
        if self.isConnected:
            self.execute('BEGIN TRANSACTION')

    def end(self):
        if self.isConnected:
            self.execute('END TRANSACTION')

    # TODO Is this a necessary function?
    # If not, delete.
    def update(self, table: str, value: dict):
        pass

    # TODO Is this a necessary function?
    # If not, delete.
    def upsert(self, table: str, value: dict):
        pass
