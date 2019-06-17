import Database.DatabaseManagement.database as db
import sqlite3 as lite
import unittest
import os


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))
        self.filePath = os.path.join(self.directory, 'testData', 'test.db')
        self.wrongFile = os.path.join(self.directory, 'testData', 'wrongfile.db')

    def test_connect_Connected(self):
        database = db.Database(self.filePath)
        self.assertTrue(database.connect())

    def test_connect_cantConnect(self):
        database = db.Database(self.wrongFile)
        self.assertFalse(database.connect())

    def test_connect_wrongMode(self):
        database = db.Database(self.filePath, 'wrongmode')
        self.assertFalse(database.connect())

    def test_disconnect(self):
        database = db.Database(self.filePath)
        database.connect()
        database.disconnect()
        self.assertIsNone(database.connection)

    def test_isConnected_Connected(self):
        database = db.Database(self.filePath)
        database.connect()
        self.assertTrue(database.isConnected)

    def test_isConnected_notConnected(self):
        database = db.Database(self.filePath)
        self.assertFalse(database.isConnected)

    def test_modifyConnection_modeChanged(self):
        database = db.Database(self.filePath)
        database.connect()
        mode_1 = database.mode
        database.modifyConnection('rw')
        self.assertNotEqual(mode_1, database.mode)

    def test_pathToURI_ReadOnlyMode(self):
        self.assertEqual(db.pathToURI('test.db'), 'file:test.db?mode=ro')

    def test_pathToURI_ReadOrWrite(self):
        self.assertEqual(db.pathToURI('test.db', 'rw'), 'file:test.db?mode=rw')

    def test_pathToURI_AbsoluteReadOnlyMode(self):
        self.assertEqual(db.pathToURI(r'C:\sqlite3\Database\test.db'), 'file:C:/sqlite3/Database/test.db?mode=ro')

    def test_pathToURI_AbsoluteReadOrWrite(self):
        self.assertEqual(db.pathToURI(r'C:\sqlite3\Database\test.db', 'rw'), 'file:C:/sqlite3/Database/test.db?mode=rw')

    def test_findingOS(self):
        # Only for windows for now.
        self.assertEqual(db.findingOS(), 'Windows')

    def test_createCursor_NoConnection(self):
        database = db.Database(self.filePath, 'test.db')

        with self.assertRaises(ConnectionError): database.createCursor()

    def test_createCursor_Connected(self):
        database = db.Database(self.filePath, 'test.db')
        database.createConnection()
        self.assertTrue(database.createCursor())

    def test_createCursor_CursorAlreadyExist(self):
        database = db.Database(self.filePath, 'test.db')
        database.createConnection()
        database.createCursor()
        with self.assertRaises(AttributeError): database.createCursor()

    def test_checkIfCursorExists_DoesExist(self):
        database = db.Database(self.filePath, 'test.db')
        database.createConnection()
        database.createCursor()
        self.assertTrue(database.checkIfCursorExists())

    def test_checkIfCursorExists_DoesNotExist(self):
        database = db.Database(self.filePath, 'test.db')
        database.createConnection()
        self.assertFalse(database.checkIfCursorExists())

    def test_closeCursor_closed(self):
        database = db.Database(self.filePath, 'test.db')
        database.createConnection()
        database.createCursor()
        self.assertTrue(database.closeCursor())

    def test_closeCursor_cantClose(self):
        database = db.Database(self.filePath, 'test.db')
        self.assertFalse(database.closeCursor())

    def test_commit_notConnected(self):
        database = db.Database(self.filePath, 'test.db')
        with self.assertRaises(ConnectionError): database.commit()

    def test_commit_noCursor(self):
        database = db.Database(self.filePath, 'test.db')
        database.createConnection()
        with self.assertRaises(AttributeError): database.commit()

    def test_commit_canCommit(self):
        database = db.Database(self.filePath, 'test.db')
        database.createConnection()
        database.createCursor()
        self.assertTrue(database.commit())

    '''
    def test_CreateTable(self):
        # This is one of the more complex test.
        # Would very much like to simplify it.
        directory = os.path.dirname(__file__)
        fileName = os.path.join(directory, 'testData', 'test.db')
        database = db.Database(fileName, 'test.db')

        #database.createConnection()
        #database.createCursor()

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
    '''


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