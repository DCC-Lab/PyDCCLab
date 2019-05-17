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

    def CreateConnection(self, mode='ro'):
        path = PathToURI(self.path, mode)
        try:
            self.conn = lite.connect(path, uri=True)
        except lite.OperationalError:
            raise Exception('Path does not work :' + path)

    def CloseConnection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        else:
            raise Exception('Connection does not exist.')

    def Commit(self):
        if self.conn is not None:
            try:
                self.conn.commit()
            except lite.OperationalError:
                raise Exception('Command could not be commited.')
        else:
            raise Exception('Connection does not exist.')

    def CreateNewDatabase(self):
        try:
            self.conn.CreateConnection(self.path, 'rwc')
            self.CloseConnection()
        except lite.OperationalError:
            raise Exception('Database could not be created : ' + str(self.path))

    def CreateCursor(self):
        if self.conn is not None:
            try:
                self.curs = self.conn.cursor()
            except lite.OperationalError:
                raise Exception('Cursor could not be created')
        else:
            raise Exception('Connection does not exist.')


def PathToURI(path, mode='ro'):
    path = pathlib.Path(path)
    if FindingOperatingSystem() == 'Windows':
        return 'file:' + parse.quote(path.as_posix(), safe=':/') + '?mode=' + mode
    if path.is_absolute():
        return path.as_uri() + '?mode=' + mode


# 'Windows' for windows, 'Linux' for linux or 'Darwin' for mac.
def FindingOperatingSystem():
    return platform.system()


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