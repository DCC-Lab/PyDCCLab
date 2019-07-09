import env
import unittest
import os
from dcclab import Database as db


class TestDatabase(env.DCCLabTestCase):
    def setUp(self):
        self.directory = self.dataDir
        self.filePath = os.path.join(str(self.tmpDir), 'unittest.db')
        self.wrongFile = os.path.join(str(self.directory), 'wrongfile.db')

        with db(self.filePath, True) as testDB:
            testDB.beginTransaction()
            testTable = {'test_table': {'column_1': 'INTEGER PRIMARY KEY', 'column_2': 'TEXT', 'column_3': 'REAL'}}
            testDB.createTable(testTable)
            testDB.commit()

            testDB.beginTransaction()
            frstValue = {'column_1': 1234, 'column_2': 'abcd', 'column_3': 0.1234}
            scndValue = {'column_1': 5678, 'column_2': 'efgh', 'column_3': 0.5678}
            testDB.insert('test_table', frstValue)
            testDB.insert('test_table', scndValue)
            testDB.commit()

    def tearDown(self):
        os.remove(self.filePath)

    def testConnectSuccessful(self):
        database = db(self.filePath)
        self.assertTrue(database.connect())
        database.disconnect()

    def testConnectUnsuccessful(self):
        database = db(self.wrongFile)
        self.assertFalse(database.connect())
        database.disconnect()

    def testConnectWithWrongMode(self):
        with self.assertRaises(Exception):
            database = db(self.filePath, 'wrongmode')
            self.assertFalse(database.connect())
            database.disconnect()

    def testConnectCreatesCursor(self):
        database = db(self.filePath)
        database.connect()
        self.assertIsNotNone(database.cursor)
        database.disconnect()

    def testDisconnectSuccesfull(self):
        database = db(self.filePath)
        database.connect()
        database.disconnect()
        self.assertFalse(database.isConnected)

    def testDisconnectRemovesCursor(self):
        database = db(self.filePath)
        database.connect()
        database.disconnect()
        self.assertIsNone(database.cursor)

    def testIsConnected(self):
        database = db(self.filePath)
        database.connect()
        self.assertTrue(database.isConnected)
        database.disconnect()

    def testIsConnectedOnInit(self):
        database = db(self.filePath)
        self.assertTrue(database.isConnected)
        database.disconnect()

    def testIsNotConnected(self):
        database = db("notADatabase")
        self.assertFalse(database.isConnected)

    def testChangeConnectionModeToValidMode(self):
        database = db(self.filePath)
        database.connect()
        database.changeConnectionMode('rw')
        self.assertNotEqual(database.mode, 'ro')
        database.disconnect()

    def testPathReadOnlyMode(self):
        database = db('unittest.db', writePermission=False)
        self.assertEqual(database.path, 'file:unittest.db?mode=ro')

    # Linux and MacOS are 'posix', windows is 'nt'.
    @unittest.skipIf(os.name == 'posix', reason='Path is a Windows Path.')
    def testWindowsPathToPosix(self):
        database = db(r'C:\sqlite3\Database\test.db', writePermission=True)
        self.assertEqual(database.path, 'file:C:/sqlite3/Database/test.db?mode=rwc')

    def testCommit(self):  # TODO Is there anything else we could test for Commit?
        database = db(self.filePath, writePermission=True)
        database.connect()

        testValue = {'column_1': 9101, 'column_2': 'plop', 'column_3': 0.9101}
        database.insert('test_table', testValue)
        database.commit()

        row = database.select('test_table', 'column_1', 'column_1=9101')
        self.assertEqual(row[0]['column_1'], 9101)
        database.disconnect()

    def testRollback(self):
        database = db(self.filePath, writePermission=True)
        database.connect()

        testValue = {'column_1': 9101, 'column_2': 'plop', 'column_3': 0.9101}
        database.beginTransaction()
        database.insert('test_table', testValue)
        database.rollback()

        database.beginTransaction()
        row = database.select('test_table', 'column_1', 'column_1=9101')
        database.endTransaction()
        self.assertFalse(row)
        database.disconnect()

    def testExecute(self):
        database = db(self.filePath, writePermission=True)
        database.connect()

        statement = 'DROP TABLE IF EXISTS test_table'
        database.execute(statement)
        database.commit()

        self.assertFalse(database.tables)
        database.disconnect()

    def testTables(self):
        database = db(self.filePath)
        database.connect()

        self.assertEqual(database.tables[0], 'test_table')

    def testSelectResultsFound(self):
        database = db(self.filePath)
        database.connect()

        rows = database.select('test_table', 'column_1', 'column_3<1')
        for row in rows:
            self.assertTrue(row['column_1'] == 1234 or 5678)

    def testSelectNoResultsFound(self):
        database = db(self.filePath)
        database.connect()

        rows = database.select('test_table', 'column_1', 'column_2="aaaa"')
        self.assertFalse(rows)

    def testCreateTable(self):
        database = db(self.filePath, writePermission=True)
        database.connect()

        newTable = {'new_table': {'column_1': 'INTEGER PRIMARY KEY', 'column_2': 'TEXT'}}
        database.createTable(newTable)
        database.commit()

        self.assertTrue(database.tables.index('new_table'))

    def testDropTable(self):
        database = db(self.filePath, writePermission=True)
        database.connect()

        database.dropTable('test_table')
        database.commit()

        self.assertFalse(database.tables)

    def testInsert(self):
        database = db(self.filePath, writePermission=True)
        database.connect()

        testValue = {'column_1': 1121, 'column_2': 'bleh', 'column_3': 0.1121}
        database.insert('test_table', testValue)
        database.commit()

        row = database.select('test_table', 'column_1', 'column_1=1121')
        self.assertEqual(row[0]['column_1'], 1121)
        database.disconnect()

    def testMode(self):
        database = db(self.filePath, writePermission=True)
        database.connect()
        self.assertEqual(database.mode, 'rwc')

    def testFetchAll(self):
        database = db(self.filePath)
        database.connect()

        database.execute('SELECT * FROM test_table')
        rows = database.fetchAll()
        for row in rows:
            self.assertTrue(row['column_1'] == 1234 or 5678)

    def testFetchOne(self):
        database = db(self.filePath)
        database.connect()

        database.execute('SELECT * FROM test_table')
        row = database.fetchOne()
        self.assertTrue(row['column_1'] == 1234)

        row = database.fetchOne()
        self.assertTrue(row['column_1'] == 5678)

        row = database.fetchOne()
        self.assertFalse(row)

    def testContextManager(self):
        with db(self.filePath) as database:
            self.assertTrue(database.isConnected)

        self.assertFalse(database.isConnected)


if __name__ == '__main__':
    unittest.main()
