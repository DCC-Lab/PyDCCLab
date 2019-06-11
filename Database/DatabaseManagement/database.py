import sqlite3 as lite
import urllib.parse as parse
import pathlib
import platform

class Database:
    def __init__(self, path, readOnly=False):
        self.path = path
        self.connection = None
        self.cursor = None
        self.readOnly = readOnly
        self.connect()

    def __del__(self):
        self.disconnect()

    def connect(self):
        if not self.isConnected:
            self.connection = lite.connect(self.path, uri=False)
            self.connection.row_factory = lite.Row
            self.cursor = self.connection.cursor()       

    def disconnect(self):
        if self.isConnected:
            self.commit()
            self.connection.close()
            self.connection = None
            self.cursor = None

    @property
    def isConnected(self):
        return self.connection is not None

    def commit(self):
        if self.isConnected:
            self.connection.commit()

    def rollback(self):
        if self.isConnected:
            self.connection.rollback()

    def execute(self, statement) -> (lite.Row):
        if self.isConnected:
            self.cursor.execute(statement)
            return self.cursor.fetchall()

    @property
    def tables(self) -> (lite.Row):
        rows = self.execute("SELECT name FROM sqlite_master WHERE type='table'")
        results = list(map(lambda row: row['name'], rows))
        return results

    def select(self, table, columns='*', condition=None) -> (lite.Row):
        if condition is None:
            rows = self.execute("SELECT {0} FROM {1}".format(columns, table))            
        else:
            rows = self.execute("SELECT {0} FROM {1} where {2}".format(columns, table, condition))
        return rows


# TODO Below is stuff to do eventually.
'''
def CreateNewDatabase(self):
    try:
        self.connection.connect(self.path, 'rwc')
        self.disconnect()
    except lite.OperationalError as error:
        raise error


def CreateTable(cursor, tableName, paramList):
    try:
        # Could this go into another function?
        command = "CREATE TABLE IF NOT EXISTS " + str(tableName) + " ("
        for param in paramList:
            command += str(param[0]) + " " + str(param[1])
            if param[2] != "":
                command += " " + str(param[2])
            command += ", "
        command = command.rstrip(", ")
        command += ")"
        cursor.execute(command)
        return True
    except connect.lite.OperationalError:
        raise Exception("An error occured while creating the table. Check if you were in the right mode.")


def DropTable(cursor, tableName):
    try:
        command = "DROP TABLE IF EXISTS " + str(tableName)
        cursor.execute(command)
        return True
    except connect.lite.OperationalError:
        raise Exception("An error occurred while deleting the table.")


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


def pathToURI(path, mode='ro'):  # TODO MacOS and Linux will have to be added eventually.
    path = pathlib.Path(path)
    if findingOS() == 'Windows':
        return 'file:' + parse.quote(path.as_posix(), safe=':/') + '?mode=' + mode
    if findingOS() == 'Darwin':
        pass
    if findingOS() == 'Linux':
        pass
    if path.is_absolute():
        return path.as_uri() + '?mode=' + mode


# 'Windows' for windows, 'Linux' for linux or 'Darwin' for mac.
# Currently not very useful but will be in the future.
def findingOS():
    return platform.system()