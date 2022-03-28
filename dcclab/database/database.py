from zipfile import ZipFile
from datetime import date
# import sqlite3 as lite
import mysql.connector as mysql
import urllib.parse as parse
import pathlib
import os
from typing import NamedTuple
import keyring
import re
import sys

"""
General-purpose Database() object.

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

class Engine(Enum):
    mysql = "mysql"
    sqlite3 = "sqlite3"

class Database:
    def __init__(self, databaseURL, writePermission=False):
        self.writePermission = writePermission
        self.databaseURL = databaseURL
        self.connection = None
        self.cursor = None
        self.databaseEngine = None

        self.database = "dcclab"
        self.host = "cafeine2.crulrg.ulaval.ca"
        self.user = "dcclab"
        self.port = None
        self.usePassword = True

        self.databaseEngine, self.sshuser, self.host, self.user, self.database = self.parseURL(databaseURL)

        self.connect()

    def parseURL(self, url):
        #mysql://sshusername:sshpassword@cafeine2.crulrg.ulaval.ca/mysqlusername:mysqlpassword@questions
        match = re.search("(.+?)://(.+?)@(.+?)/(.+?)@(.+)", url)
        if match is not None:
            protocol = Engine.mysql
            sshuser = match.group(2)
            host = match.group(3)
            mysqluser = match.group(4)
            database = match.group(5)
            return (protocol, sshuser, host, mysqluser, database)
        else:
            return (Engine.sqlite3, None, "127.0.0.1", None, url)

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
                if self.databaseEngine == Engine.sqlite3:
                    self.connection = lite.connect(
                        self.database, uri=True, isolation_level=None, detect_types=lite.PARSE_DECLTYPES)
                    self.connection.row_factory = lite.Row
                    self.cursor = self.connection.cursor()
                else:
                    if self.usePassword is True:
                        serviceName = "mysql-{0}".format(self.host)
                        pwd = keyring.get_password(serviceName, self.user)
                        if pwd is None:
                            raise Exception(""" Set the password in the system password manager on the command line with:
                            python -m keyring set {0} {1}""".format(serviceName, self.user))
                    else:
                        pwd = None

                    actualHost = self.host
                    if self.host == "cafeine2.crulrg.ulaval.ca":
                        from dcclab import Cafeine
                        actualHost = "127.0.0.1"
                        self.server = Cafeine()
                        self.port = self.server.startMySQLTunnel()
                        print("Forwarding 127.0.0.1:{2} to {0}@{1}:3306 through SSH tunnel".format(self.user, self.host, self.port))
                    else:
                        self.port = 3306

                    self.connection = mysql.connect(host=actualHost,
                                                    port=self.port,
                                                     database=self.database,
                                                     user=self.user,
                                                     password=pwd,
                                                     autocommit=True,
                                                     use_pure=True)

                    self.cursor = self.connection.cursor(dictionary=True)

                self.enforceForeignKeys()

            return True
        except Exception as err:
            # Cleanup
            print(err)
            if self.connection is not None:
                self.connection.close()
                self.server.stopMySQLTunnel()
                self.cursor = None

            return False

    def disconnect(self):
        if self.isConnected:
            self.commit()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def enforceForeignKeys(self):
        if self.databaseEngine == Engine.sqlite3:
            self.execute("PRAGMA foreign_keys = ON")
        else:
            self.execute("set foreign_key_checks = 1")

    def disableForeignKeys(self):
        if self.databaseEngine == Engine.sqlite3:
            self.execute("PRAGMA foreign_keys = OFF")
        else:
            self.execute("set foreign_key_checks = 0")


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


    def asynchronous(self):
        # Asynchronous mode means the database doesn't wait for
        # something to be entirely written before it begins
        # to write something else. It has the potential of corrupting entries
        # if the database crashed or there is a power failure.
        # However, asynchronus mode is much faster.
        if self.isConnected:
            self.execute('PRAGMA synchronous = OFF')

    def beginTransaction(self):
        if self.databaseEngine == Engine.mysql:
            if self.isConnected:
                self.execute('BEGIN')
        else:
            self.execute('BEGIN TRANSACTION')

    def endTransaction(self):
        if self.databaseEngine == Engine.mysql:
            if self.isConnected:
                self.execute('END')
        else:
            self.execute('END TRANSACTION')

    @property
    def isConnected(self):
        return self.connection is not None

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
            self.connection.commit()

    def rollback(self):
        if self.isConnected:
            self.connection.rollback()

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
        if self.databaseEngine == Engine.mysql:
            self.execute("show tables")
            rows = self.fetchAll()
            results = [ list(row.values())[0] for row in rows ]
            return results
        else:
            self.execute(".tables")
            rows = self.fetchAll()
            results = [ list(row.values())[0] for row in rows ]
            return results

    def columns(self, table) -> list:  # FixMe Find a better name?
        self.execute('SELECT * FROM "{}"'.format(table))
        columns = [description[0] for description in self.cursor.description]
        return columns

    def select(self, table, columns='*', condition=None):
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

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    db = Database("mysql://dcclab@cafeine2.crulrg.ulaval.ca/dcclab@raman")
    db.execute('select * from files')
    print(db.fetchAll())
    # db = Database("/Users/dccote/GitHub/PyVino/raman.db")
    # db.execute('select * from files')
    # print(db.fetchAll())

