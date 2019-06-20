from dcclab import database as db
import unittest
import os


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(__file__)
        self.filePath = os.path.join(self.directory, 'unittest.db')
        self.wrongFile = os.path.join(self.directory, 'wrongfile.db')

        # For testing purpose, a fake database has to be built.
        # We have to create a fake table and add fake data into it.
        self.database = db.Database(self.filePath, 'rwc')
        self.database.connect()

        testTable = {'test_table': {'column_1': 'INTEGER PRIMARY KEY', 'column_2': 'TEXT', 'column_3': 'REAL'}}
        self.database.createTable(testTable)
        self.database.commit()

        frstValue = {'column_1': 1234, 'column_2': 'abcd', 'column_3': 0.1234}
        scndValue = {'column_1': 5678, 'column_2': 'efgh', 'column_3': 0.5678}
        self.database.insert('test_table', frstValue)
        self.database.insert('test_table', scndValue)
        self.database.commit()
        self.database.disconnect()

    def tearDown(self):
        os.remove(self.filePath)

    def testConnectSuccesfull(self):
        database = db.Database(self.filePath)
        self.assertTrue(database.connect())
        database.disconnect()

    def testConnectUnsuccesfull(self):
        database = db.Database(self.wrongFile)
        self.assertFalse(database.connect())
        database.disconnect()

    def testConnectWithWrongMode(self):
        database = db.Database(self.filePath, 'wrongmode')
        self.assertFalse(database.connect())
        database.disconnect()

    def testConnectCreatesCursor(self):
        database = db.Database(self.filePath)
        database.connect()
        self.assertIsNotNone(database.cursor)
        database.disconnect()

    def testDisconnectSuccesfull(self):
        database = db.Database(self.filePath)
        database.connect()
        database.disconnect()
        self.assertFalse(database.isConnected)

    def testDisconnectRemovesCursor(self):
        database = db.Database(self.filePath)
        database.connect()
        database.disconnect()
        self.assertIsNone(database.cursor)

    def testIsConnected(self):
        database = db.Database(self.filePath)
        database.connect()
        self.assertTrue(database.isConnected)
        database.disconnect()

    def testIsNotConnected(self):
        database = db.Database(self.filePath)
        self.assertFalse(database.isConnected)

    def testChangeConnectionModeToValidMode(self):
        database = db.Database(self.filePath, 'ro')
        database.connect()
        database.changeConnectionMode('rw')
        self.assertNotEqual(database.mode, 'ro')
        database.disconnect()

    def testPathReadOnlyMode(self):
        database = db.Database('unittest.db', 'ro')
        self.assertEqual(database.path, 'file:unittest.db?mode=ro')

    def testWindowsPathToPosix(self):
        database = db.Database(r'C:\sqlite3\Database\test.db', 'rwc')
        self.assertEqual(database.path, 'file:C:/sqlite3/Database/test.db?mode=rwc')

    def testCommit(self):  # TODO Is there anything else we could test for Commit?
        database = db.Database(self.filePath, 'rw')
        database.connect()
        testValue = {'column_1': 9101, 'column_2': 'plop', 'column_3': 0.9101}
        database.insert('test_table', testValue)
        database.commit()

        row = database.select('test_table', 'column_1', 'column_1=9101')
        self.assertEqual(row[0]['column_1'], 9101)
        database.disconnect()

    def testRollback(self):  # TODO Is there anything else we could test for Rollback?
        database = db.Database(self.filePath, 'rw')
        database.connect()
        testValue = {'column_1': 9101, 'column_2': 'plop', 'column_3': 0.9101}
        database.insert('test_table', testValue)
        database.rollback()
        database.commit()

        row = database.select('test_table', 'column_1', 'column_1=9101')
        self.assertFalse(row)
        database.disconnect()

    # How to test database.execute()?
    def testExecute(self):
        pass

    # How to test database.tables?
    def testTables(self):
        pass

    # How to test database.select()?
    def testSelect(self):
        pass

    # How to test database.createTable()?
    def testCreateTable(self):
        pass

    # How to test database.dropTable()?
    def testDropTable(self):
        pass

    # How to test database.insert()?
    def testInsert(self):
        pass

    '''
    def test_CreateTable(self):
        # This is one of the more complex test.
        # Would very much like to simplify it.
        directory = os.path.dirname(__file__)
        fileName = os.path.join(directory, 'testData', 'test.db')
        database = db.obsolete(fileName, 'test.db')

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