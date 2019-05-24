import sqlite3 as lite
import urllib.parse as parse
import pathlib
import platform


class Database:
    def __init__(self, path, name=''):
        self.path = path
        self.name = name
        self.conn = None
        self.curs = None

    def createConnection(self, mode='ro'):
        if self.checkConnection() is False:
            path = pathToURI(self.path, mode)
            try:
                self.conn = lite.connect(path, uri=True)
                return 'connected'
            except lite.OperationalError as error:
                raise error
        else:
            raise Exception('Already connected to a database : ' + self.name + " : " + self.path)

    def closeConnection(self):
        if self.checkConnection():
            self.closeCursor()
            self.conn.close()
            self.conn = None
            return 'disconnected'
        else:
            raise Exception('Connection does not exist.')

    def checkConnection(self):
        if self.conn is not None:
            return True
        else:
            return False

    def changeConnectionMode(self, mode):
        if self.checkConnection():
            self.closeConnection()
            try:
                self.createConnection(mode)
                return True
            except lite.OperationalError as error:
                raise error
        else:
            return False

    def createCursor(self):
        if self.checkConnection():
            try:
                self.closeCursor()
                self.curs = self.conn.cursor()
                return True
            except lite.OperationalError as error:
                raise error
        else:
            raise Exception('Connection does not exist.')

    def closeCursor(self):
        if self.curs is not None:
            self.curs.close()
            self.curs = None
            return True
        else:
            return False

    def commit(self):
        if self.checkConnection() and self.curs is not None:
            try:
                self.conn.commit()
                return True
            except lite.OperationalError as error:
                raise error
        else:
            raise Exception('Connection/cursor does not exist.')

# TODO Below is stuff to do eventually.
'''
def CreateNewDatabase(self):
    try:
        self.conn.createConnection(self.path, 'rwc')
        self.closeConnection()
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


def pathToURI(path, mode='ro'):
    path = pathlib.Path(path)
    if findingOS() == 'Windows':
        return 'file:' + parse.quote(path.as_posix(), safe=':/') + '?mode=' + mode
    if path.is_absolute():
        return path.as_uri() + '?mode=' + mode


# 'Windows' for windows, 'Linux' for linux or 'Darwin' for mac.
# Currently not very useful but will be in the future.
def findingOS():
    return platform.system()