import env
from dcclab import database as db
import unittest
import os


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.dirname(__file__)
        self.filePath = os.path.join(self.directory, 'unittest.db')
        self.wrongFile = os.path.join(self.directory, 'wrongfile.db')

        # For testing purpose, a fake database has to be built.
        self.database = db.Database(self.filePath, 'rwc')
        self.database.connect()

        # We create a fake table.
        testTable = {'test_table': {'column_1': 'INTEGER PRIMARY KEY', 'column_2': 'TEXT', 'column_3': 'REAL'}}
        self.database.createTable(testTable)
        self.database.commit()

        # We create fake data and insert it into the table.
        frstValue = {'column_1': 1234, 'column_2': 'abcd', 'column_3': 0.1234}
        scndValue = {'column_1': 5678, 'column_2': 'efgh', 'column_3': 0.5678}
        self.database.insert('test_table', frstValue)
        self.database.insert('test_table', scndValue)
        self.database.commit()
        self.database.disconnect()

    def tearDown(self):
        # At the end of the test, we delete the database.
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

    def testExecute(self):
        database = db.Database(self.filePath, 'rw')
        database.connect()

        statement = 'DROP TABLE IF EXISTS test_table'
        database.execute(statement)
        database.commit()

        self.assertFalse(database.tables)
        database.disconnect()

    def testTables(self):
        database = db.Database(self.filePath)
        database.connect()

        self.assertEqual(database.tables[0], 'test_table')

    def testSelectResultsFound(self):
        database = db.Database(self.filePath)
        database.connect()

        rows = database.select('test_table', 'column_1', 'column_3<1')
        for row in rows:
            self.assertTrue(row['column_1'] == 1234 or 5678)

    def testSelectNoResultsFound(self):
        database = db.Database(self.filePath)
        database.connect()

        rows = database.select('test_table', 'column_1', 'column_2="aaaa"')
        self.assertFalse(rows)

    def testCreateTable(self):
        database = db.Database(self.filePath, 'rw')
        database.connect()

        newTable = {'new_table': {'column_1': 'INTEGER PRIMARY KEY', 'column_2': 'TEXT'}}
        database.createTable(newTable)
        database.commit()

        self.assertTrue(database.tables.index('new_table'))

    def testDropTable(self):
        database = db.Database(self.filePath, 'rw')
        database.connect()

        database.dropTable('test_table')
        database.commit()

        self.assertFalse(database.tables)

    def testInsert(self):
        database = db.Database(self.filePath, 'rw')
        database.connect()

        testValue = {'column_1': 1121, 'column_2': 'bleh', 'column_3': 0.1121}
        database.insert('test_table', testValue)
        database.commit()

        row = database.select('test_table', 'column_1', 'column_1=1121')
        self.assertEqual(row[0]['column_1'], 1121)
        database.disconnect()

    def testMode(self):
        database = db.Database(self.filePath, 'rw')
        database.connect()

        self.assertEqual(database.mode, 'rw')

    def testFetchAll(self):
        database = db.Database(self.filePath)
        database.connect()

        database.execute('SELECT * FROM test_table')
        rows = database.fetchAll()
        for row in rows:
            self.assertTrue(row['column_1'] == 1234 or 5678)

    def testFetchOne(self):
        database = db.Database(self.filePath)
        database.connect()

        database.execute('SELECT * FROM test_table')
        row = database.fetchOne()
        self.assertTrue(row['column_1'] == 1234)

        row = database.fetchOne()
        self.assertTrue(row['column_1'] == 5678)

        row = database.fetchOne()
        self.assertFalse(row)


if __name__ == '__main__':
    unittest.main()
