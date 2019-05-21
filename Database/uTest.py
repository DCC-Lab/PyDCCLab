import Database.database as db
import sqlite3 as lite
import unittest
import os


class TestDatabase(unittest.TestCase):
    def test_createConnection(self):
        directory = os.path.dirname(__file__)
        fileName = os.path.join(directory, 'data', 'test.db')

        database = db.Database(fileName, 'test.db')
        self.assertEqual(database.createConnection(), 'connected')
        database.closeConnection()

        database = db.Database(fileName, 'test.db')
        database.createConnection()
        with self.assertRaises(Exception): database.createConnection()

        fileName = os.path.join(directory, 'data', 'tst.db')
        database = db.Database(fileName, 'test.db')
        with self.assertRaises(Exception): database.createConnection()

    def test_closeConnection(self):
        directory = os.path.dirname(__file__)
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        self.assertEqual(database.closeConnection(), 'disconnected')

        with self.assertRaises(Exception): database.closeConnection()

    def test_checkConnection(self):
        directory = os.path.dirname(__file__)
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        self.assertTrue(database.checkConnection())

        database.closeConnection()
        self.assertFalse(database.checkConnection())

    def test_changeConnection(self):
        directory = os.path.dirname(__file__)
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')

        pass

    def test_patToURI(self):
        self.assertEqual(db.pathToURI('test.db'), 'file:test.db?mode=ro')
        self.assertEqual(db.pathToURI('test.db', 'rw'), 'file:test.db?mode=rw')
        self.assertEqual(db.pathToURI(r'C:\sqlite3\Database\test.db'), 'file:C:/sqlite3/Database/test.db?mode=ro')
        self.assertEqual(db.pathToURI(r'C:\sqlite3\Database\test.db', 'rw'), 'file:C:/sqlite3/Database/test.db?mode=rw')

    def test_ResolvingPlatform(self):
        # Only for windows for now.
        self.assertEqual(db.FindingOperatingSystem(), 'Windows')

    def test_CreateCursor(self):
        connection_test = db.CreateConnection('test.db')
        self.assertIs(type(db.CreateCursor(connection_test)), lite.Cursor)
        db.CloseConnection(connection_test)

        with self.assertRaises(Exception): db.CreateCursor('')

    def test_CreateTable(self):
        # Setting up the test.
        connection_test = db.CreateConnection('test.db', 'rw')
        cursor_test = db.CreateCursor(connection_test)
        name_test = "persons"
        paramList_test = [["id", "INT(20)", "PRIMARY KEY"], ["firstname", "TEXT(30)", ""], ["lastname", "TEXT(30)", ""]]

        self.assertTrue(db.CreateTable(cursor_test, name_test, paramList_test))     # Table does not exist.
        db.CommitConnection(connection_test)

        self.assertTrue(db.CreateTable(cursor_test, name_test, paramList_test))     # Table does exist.
        db.CommitConnection(connection_test)
        db.DropTable(cursor_test, name_test)
        db.CommitConnection(connection_test)
        db.CloseConnection(connection_test)

        connection_test = db.CreateConnection('test.db', 'ro')
        cursor_test = db.CreateCursor(connection_test)
        with self.assertRaises(Exception): db.CreateTable(cursor_test, name_test, paramList_test)   # Wrong mode.
        db.DropTable(cursor_test, name_test)
        db.CommitConnection(connection_test)
        db.CloseConnection(connection_test)

    def test_DropTable(self):
        connection_test = db.CreateConnection('test.db', 'rw')
        cursor_test = db.CreateCursor(connection_test)
        name_test = "persons"
        paramList_test = [["id", "INT(20)", "PRIMARY KEY"], ["firstname", "TEXT(30)", ""], ["lastname", "TEXT(30)", ""]]
        db.CreateTable(cursor_test, name_test, paramList_test)
        db.CommitConnection(connection_test)
        db.CloseConnection(connection_test)

        connection_test = db.CreateConnection('test.db', 'ro')
        cursor_test = db.CreateCursor(connection_test)
        with self.assertRaises(Exception): db.DropTable(cursor_test, name_test)  # Wrong mode.
        db.CommitConnection(connection_test)
        db.CloseConnection(connection_test)

        connection_test = db.CreateConnection('test.db', 'rw')
        cursor_test = db.CreateCursor(connection_test)
        self.assertTrue(db.DropTable(cursor_test, name_test))   # Table does exist.
        db.CommitConnection(connection_test)

        self.assertTrue(db.DropTable(cursor_test, name_test))   # Table des not exist.
        db.CommitConnection(connection_test)
        db.CloseConnection(connection_test)

    def test_ListAllTables(self):
        connection_test = db.CreateConnection('test.db')
        cursor_test = db.CreateCursor(connection_test)

        self.assertGreater(len(db.ListAllTables(cursor_test)), 0)


if __name__ == '__main__':
    unittest.main()

    # cursor.execute('CREATE TABLE table_1 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT(30))')
    # cursor.execute('CREATE TABLE table_2 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT(30))')
    # cursor.execute('CREATE TABLE table_3 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT(30), age INTEGER(3))')
    #cursor.execute("DROP TABLE 'sqlite_sequence'")
    #connection.commit()

    # Extracting table names
    '''
    tableNames = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = []
    for name in tableNames:
        newname = name
        newname = str(newname).replace('(', '')
        newname = newname.replace("'", "")
        newname = newname.replace(')', '')
        newname = newname.replace(',', '')
        tables.append(newname)
    '''

    # Extracting columns name in a table
    '''
    for table in tables:
        reader = cursor.execute("SELECT * FROM {}".format(table))
        for x in reader.description:
            print(x[0])
    connection.close()
    '''