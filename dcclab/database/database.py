from zipfile import ZipFile
from datetime import date
import sqlite3 as lite
import urllib.parse as parse
import pathlib
import os
from typing import NamedTuple

"""
General-purpose Databse() object.

The database is ready to use (i.e. `connected`) upon creation.
To begin using the `Database`, making queries or inserting into it,
use the exposed API (e.g., `select(table, columns, condition) -> lite.Row:`)
or execute an explicit SQL command (e.g., `    execute(statement)`).
To create a new database, a `Database` object has to be created with
`writePermission=True`. If it does not exist yet, the database will
be created at the `Database.path` location (in **URI**).

If you want to create new tables, a dictionary(*of dictionaries*) 
containing the tables' name and their associated keys/types has 
to be passed to `Database.createTable()`. It should be in the form:

```
{table_1: {key_1: type, key_2: type, key_3: type}, 
table_2: {key_1: type, key_2: type, key_3: type}, ...}
```

The `keys` property of the `Metadata` object, and its underlying
objects, already handle the creation of the above dictionary.
Knowing that, you can quickly create a table with
`Database.createTable(Metadata.keys)`. To drop a table, use the
`Database.dropTable()` function, passing it only the table's name.
To insert data into the database, use `Database.insert()`, passing
it the table into which you want to insert and a dictionary of keys
with their associated values.

`Database` objects are created with `isolation_level = None` by default.
This is because `PEP` requires `python` to handle autocommits and
transactions as a default stance. By setting `isolation_level` to `None`,
we revert from `PEP` autocommit to `SQLite` autocommits. From there, it
is possible, using `Database.begin()`, `Database.end()`, `Database.commit()`
and `Database.rollBack()`, to manually control the transactions and commits.
This allows us to greatly increase insert speed into the database.
Similarly, `Database.asynchronous()` also changes properties of the
database to allow for faster insert. **HOWEVER**, this is a dangerous
function to use because it increases the chances of corrupt data in the
database should the server crash or should there be a power failure.

The `mtpDatabase` script in dcclab is meant to create the mtp.db
database on the cafeine2 server, under dcclab/database. It contains
the metadata of the ** Molecular Tools Platform ** `.csv` files under
dcclab/database as well as the metadata from their `.czi` files in the
cafeine2 server.

"""

from enum import Enum

class Type(Enum):
    Null = "NULL"
    Integer = "INTEGER"
    Real = "REAL"
    Float = "REAL"
    Text = "TEXT"
    String = "TEXT"
    Blob = "BLOB"

class Constraint(Enum):
    Primary = "PRIMARY KEY"
    Default = ""

class Column(NamedTuple):
    name: str
    type: Type
    constraint: Constraint = Constraint.Default

class Database:
    def __init__(self, databasePath, writePermission=False):
        if writePermission is True:
            # Possible modes are read-only, read write and read write create
            # which are 'ro', 'rw', and 'rwc' respectively
            mode = 'rwc'
        elif writePermission is False:
            mode = 'ro'
        else:
            raise ValueError("writePermission parameter must be true or false")

        self.__mode = mode
        self.__databasePath = databasePath
        self.__connection = None
        self.cursor = None

        if not os.path.exists(databasePath) and not writePermission:
            raise ValueError(f"The database {databasePath} does not exist and cannot be created because writePermission is set to False")
        
        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def path(self):
        path = pathlib.Path(self.__databasePath)
        return 'file:{}?mode={}'.format(parse.quote(path.as_posix(), safe=':/'), self.mode)

    @property
    def mode(self):
        return self.__mode

    def connect(self):
        try:
            if not self.isConnected:
                self.__connection = lite.connect(
                    self.path, uri=True, isolation_level=None)
                self.__connection.row_factory = lite.Row
                self.cursor = self.__connection.cursor()
            return True
        except:
            # Cleanup
            if self.__connection is not None:
                self.__connection.close()
                self.cursor = None

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

    def setPermissionToWrite(self):
        if self.isConnected:
            self.disconnect()
        self.__mode = 'rwc'
        self.connect()

    def setPermissionToReadOnly(self):
        if self.isConnected:
            self.disconnect()
        self.__mode = 'ro'
        self.connect()

    def changeConnectionMode(self, mode):
        if mode == 'ro':
            self.setPermissionToReadOnly()
        elif mode == 'rwc' or mode == 'rw':
            self.setPermissionToWrite()

    def commit(self):
        if self.isConnected:
            self.__connection.commit()

    def rollback(self):
        if self.isConnected:
            self.__connection.rollback()

    def execute(self, statement):
        if self.isConnected:
            self.cursor.execute(statement)

    def fetchAll(self) -> lite.Row:
        if self.isConnected:
            return self.cursor.fetchall()

    def fetchOne(self) -> lite.Row:
        if self.isConnected:
            return self.cursor.fetchone()

    @property
    def tables(self) -> list:
        self.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rows = self.fetchAll()
        results = list(map(lambda row: row['name'], rows))
        return results

    def columns(self, table) -> list:  # FixMe Find a better name?
        self.execute('SELECT * FROM "{}"'.format(table))
        columns = [description[0] for description in self.cursor.description]
        return columns

    def select(self, table, columns='*', condition=None) -> lite.Row:
        if condition is None:
            self.execute("SELECT {0} FROM {1}".format(columns, table))
        else:
            self.execute("SELECT {0} FROM {1} WHERE {2}".format(
                columns, table, condition))
        return self.fetchAll()

    def createTable(self, metadata: dict):
        if self.isConnected:
            for table, keys in metadata.items():
                statement = 'CREATE TABLE IF NOT EXISTS "{}" ('.format(table)
                attributes = []
                for key, keyType in keys.items():
                    attributes.append('{} {}'.format(key, keyType))
                statement += ",".join(attributes) + ")"
                self.execute(statement)

    def createSimpleTable(self, name, columns):
        if self.isConnected:
            statement = f'CREATE TABLE IF NOT EXISTS "{name}" '

            colStatements = []
            for c in columns:
                colStatements.append(f"{c.name} {c.type.value} {c.constraint.value}")

            statement += '(' + ','.join(colStatements) + ')'
            self.execute(statement)

    def dropTable(self, table: str):
        if self.isConnected:
            statement = 'DROP TABLE IF EXISTS "{}"'.format(table)
            self.execute(statement)

    def insert(self, table: str, entry: dict):
        if self.isConnected:
            lstKeys = []
            lstValues = []
            for key in entry.keys():
                lstKeys.append('"{}"'.format(str(key)))
                lstValues.append('"{}"'.format(str(entry[key])))
            keys = ','.join(lstKeys)
            values = ','.join(lstValues)
            statement = 'INSERT OR REPLACE INTO "{}" ({}) VALUES ({})'.format(
                table, keys, values)
            self.execute(statement)

    def asynchronous(self):
    # Asynchronous mode means the database doesn't wait for 
    # something to be entirely written before it begins
    # to write something else. It has the potential of corrupting entries
    # if the database crashed or there is a power failure. 
    # However, asynchronus mode is much faster.
        if self.isConnected:
                self.execute('PRAGMA synchronous = OFF')

    def beginTransaction(self):
    # With isolation_level = None for our connection, we disable 
    # the python auto-handling of BEGIN, etc. We reset to the
    # default SQLite handling. By default, SQLite is in auto-commit mode.
    # It means that for each command, SQLite starts, processes, and
    # commits the transaction automatically. By issuing a BEGIN, we
    # override this and manually handle transaction commits. This allows
    # faster writing to the database.
        if self.isConnected:
            self.execute('BEGIN TRANSACTION')

    def endTransaction(self):
        if self.isConnected:
            self.execute('END TRANSACTION')

    def createArchive(self):
        # Before using this function, make sure that you have enough disk space available.
        # TODO Should we check for available disk space?
        if self.__rows is not None:
            archive = '{}_query_archive.zip'.format(str(date.today()).replace('-', ''))
            with ZipFile(archive, 'w') as zeep:
                for row in self.__rows:
                    filePath = row['file_path']
                    fileName = os.path.basename(filePath)
                    zeep.write(filePath, fileName)

    # TODO Is this a necessary function?
    # If not, delete.
    def update(self, table: str, value: dict):
        pass

    # TODO Is this a necessary function?
    # If not, delete.
    def upsert(self, table: str, value: dict):
        pass
