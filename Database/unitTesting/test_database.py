import Database.management_database.database as db
import sqlite3 as lite
import unittest
import os


class TestDatabase(unittest.TestCase):
    def test_createConnection_connected(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')

        database = db.Database(fileName, 'test.db')
        self.assertEqual(database.createConnection(), 'connected')
        database.closeConnection()

    def test_createConnection_AlreadyConnected(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')

        database = db.Database(fileName, 'test.db')
        self.assertEqual(database.createConnection(), 'connected')
        database.closeConnection()

        database = db.Database(fileName, 'test.db')
        database.createConnection()
        with self.assertRaises(Exception): database.createConnection()

    def test_createConnection_CantConnect(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'tst.db')
        database = db.Database(fileName, 'test.db')
        with self.assertRaises(lite.OperationalError): database.createConnection()

    def test_closeConnection_disconnected(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        self.assertEqual(database.closeConnection(), 'disconnected')

    def test_cloeConnection_NoConnection(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')

        with self.assertRaises(Exception): database.closeConnection()

    def test_closeConnection_CantDisconnect(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'tst.db')
        database = db.Database(fileName, 'test.db')

        with self.assertRaises(Exception): database.closeConnection()

    def test_closeConnection_CursorExists(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        database.createCursor()
        with self.assertRaises(Exception): database.closeConnection()

    def test_checkIfIsConnected_IsConnected(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        self.assertTrue(database.checkIfIsConnected())

    def test_checkIfIsConnected_IsNotConnected(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        database.closeConnection()

        self.assertFalse(database.checkIfIsConnected())

    def test_changeConnectionMode_NoConnection(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')

        self.assertFalse(database.changeConnectionMode('rw'))

    def test_changeConnectionMode_ModeChanged(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')

        database.createConnection()
        self.assertTrue(database.changeConnectionMode('rw'))

    def test_changeConnectionMode_InvalidMode(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()

        with self.assertRaises(lite.OperationalError): database.changeConnectionMode('abcd')

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
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')

        with self.assertRaises(Exception): database.createCursor()

    def test_createCursor_Connected(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        self.assertTrue(database.createCursor())

    def test_createCursor_CursorAlreadyExist(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        database.createCursor()
        with self.assertRaises(Exception): database.createCursor()

    def test_checkIfCursorExists_DoesExist(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        database.createCursor()
        self.assertTrue(database.checkIfCursorExists())

    def test_checkIfCursorExists_DoesNotExist(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        self.assertFalse(database.checkIfCursorExists())

    def test_closeCursor_closed(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        database.createCursor()
        self.assertTrue(database.closeCursor())

    def test_closeCursor_cantClose(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        self.assertFalse(database.closeCursor())

    def test_commit_notConnected(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        with self.assertRaises(Exception): database.commit()

    def test_commit_noCursor(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        with self.assertRaises(Exception): database.commit()

    def test_commit_canCommit(self):
        directory = os.path.dirname(os.path.dirname(__file__))
        fileName = os.path.join(directory, 'data', 'test.db')
        database = db.Database(fileName, 'test.db')
        database.createConnection()
        database.createCursor()
        self.assertTrue(database.commit())

    '''
    def test_CreateTable(self):
        # This is one of the more complex test.
        # Would very much like to simplify it.
        directory = os.path.dirname(__file__)
        fileName = os.path.join(directory, 'data', 'test.db')
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